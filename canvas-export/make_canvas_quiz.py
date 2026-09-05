#!/usr/bin/env python3
"""Build Canvas-importable quizzes from a chapter's questions file.

For each NN-name.questions.yml (see 00-template.questions.yml) this writes:
  NN-name.qti.zip  - QTI 1.2 package (Canvas: Import Course Content -> QTI .zip)
  NN-name.csv      - flat review sheet of the same questions

Question types: mcq (4 options, 1 correct), short (accepted answers),
applied (essay, manually marked). Questions carrying `flag:` are skipped
with a warning until the flag is resolved.

Usage:
  python3 make_canvas_quiz.py [NN-name.questions.yml ...]
With no arguments, every *.questions.yml in this directory except the
00-template is processed.
"""

import csv
import sys
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required: pip install pyyaml")

HERE = Path(__file__).resolve().parent


def qti_item(q, n):
    """One <item> element (QTI 1.2, Canvas dialect) for question dict q."""
    ident = escape(str(q.get("id", f"q{n}")))
    text = escape(q["text"]).strip()
    qtype = q["type"]
    meta = {
        "mcq": "multiple_choice_question",
        "short": "short_answer_question",
        "applied": "essay_question",
    }[qtype]
    head = (
        f'    <item ident="{ident}" title="Question {n}">\n'
        "      <itemmetadata><qtimetadata>\n"
        "        <qtimetadatafield><fieldlabel>question_type</fieldlabel>"
        f"<fieldentry>{meta}</fieldentry></qtimetadatafield>\n"
        "        <qtimetadatafield><fieldlabel>points_possible</fieldlabel>"
        "<fieldentry>1</fieldentry></qtimetadatafield>\n"
        "      </qtimetadata></itemmetadata>\n"
    )
    mattext = f'<material><mattext texttype="text/plain">{text}</mattext></material>'

    if qtype == "mcq":
        opts = q["options"]
        if len(opts) != 4:
            raise ValueError(f"{ident}: mcq needs exactly 4 options")
        correct = int(q["correct"])
        if not 1 <= correct <= 4:
            raise ValueError(f"{ident}: correct must be 1-4")
        labels = "".join(
            f'          <response_label ident="{1000 + i}"><material>'
            f'<mattext texttype="text/plain">{escape(o)}</mattext>'
            "</material></response_label>\n"
            for i, o in enumerate(opts, start=1)
        )
        body = (
            "      <presentation>\n"
            f"        {mattext}\n"
            '        <response_lid ident="response1" rcardinality="Single">\n'
            "        <render_choice>\n"
            f"{labels}"
            "        </render_choice>\n"
            "        </response_lid>\n"
            "      </presentation>\n"
            "      <resprocessing>\n"
            '        <outcomes><decvar maxvalue="100" minvalue="0"'
            ' varname="SCORE" vartype="Decimal"/></outcomes>\n'
            '        <respcondition continue="No"><conditionvar>'
            f'<varequal respident="response1">{1000 + correct}</varequal>'
            "</conditionvar>"
            '<setvar action="Set" varname="SCORE">100</setvar>'
            "</respcondition>\n"
            "      </resprocessing>\n"
        )
    elif qtype == "short":
        answers = q.get("answers") or []
        if not answers:
            raise ValueError(f"{ident}: short question needs accepted answers")
        conds = "".join(
            '        <respcondition continue="No"><conditionvar>'
            f'<varequal respident="response1">{escape(str(a))}</varequal>'
            "</conditionvar>"
            '<setvar action="Set" varname="SCORE">100</setvar>'
            "</respcondition>\n"
            for a in answers
        )
        body = (
            "      <presentation>\n"
            f"        {mattext}\n"
            '        <response_str ident="response1" rcardinality="Single">'
            '<render_fib><response_label ident="answer1"/></render_fib>'
            "</response_str>\n"
            "      </presentation>\n"
            "      <resprocessing>\n"
            '        <outcomes><decvar maxvalue="100" minvalue="0"'
            ' varname="SCORE" vartype="Decimal"/></outcomes>\n'
            f"{conds}"
            "      </resprocessing>\n"
        )
    else:  # applied -> essay, manually marked
        body = (
            "      <presentation>\n"
            f"        {mattext}\n"
            '        <response_str ident="response1" rcardinality="Single">'
            '<render_fib><response_label ident="answer1"'
            ' rshuffle="No"/></render_fib></response_str>\n'
            "      </presentation>\n"
        )
    return head + body + "    </item>\n"


def build_qti(data, out_zip):
    items = []
    n = 0
    for q in data["questions"]:
        if q.get("flag"):
            print(f"  SKIPPED (flagged): {q.get('id')}: {q['flag']}")
            continue
        n += 1
        items.append(qti_item(q, n))
    title = escape(data.get("quiz_title", out_zip.stem))
    quiz = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<questestinterop xmlns="http://www.imsglobal.org/xsd/ims_qtiasiv1p2">\n'
        f'  <assessment ident="{out_zip.stem}" title="{title}">\n'
        '  <section ident="root_section">\n'
        + "".join(items)
        + "  </section>\n  </assessment>\n</questestinterop>\n"
    )
    manifest = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<manifest identifier="{out_zip.stem}-manifest"'
        ' xmlns="http://www.imsglobal.org/xsd/imscp_v1p1">\n'
        "  <organizations/>\n"
        "  <resources>\n"
        f'    <resource identifier="{out_zip.stem}-quiz"'
        ' type="imsqti_xmlv1p2" href="quiz.xml"><file href="quiz.xml"/></resource>\n'
        "  </resources>\n</manifest>\n"
    )
    with zipfile.ZipFile(out_zip, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("imsmanifest.xml", manifest)
        z.writestr("quiz.xml", quiz)
    return n


def build_csv(data, out_csv):
    cols = [
        "number", "id", "type", "section", "difficulty", "question",
        "option_a", "option_b", "option_c", "option_d", "correct",
        "accepted_answers", "sample_answer", "flag",
    ]
    with out_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(cols)
        for n, q in enumerate(data["questions"], start=1):
            opts = (q.get("options") or []) + [""] * 4
            w.writerow([
                n, q.get("id", ""), q["type"], q.get("section", ""),
                q.get("difficulty", ""), q["text"].strip(),
                opts[0], opts[1], opts[2], opts[3],
                q.get("correct", ""),
                "; ".join(str(a) for a in (q.get("answers") or [])),
                (q.get("sample_answer") or "").strip(),
                q.get("flag", ""),
            ])


def main(argv):
    files = [Path(a) for a in argv] or sorted(
        p for p in HERE.glob("*.questions.yml") if not p.name.startswith("00-")
    )
    if not files:
        print("No *.questions.yml files found (template is skipped).")
        return
    for path in files:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        stem = path.name.removesuffix(".questions.yml")
        print(f"{path.name}:")
        n = build_qti(data, path.with_name(f"{stem}.qti.zip"))
        build_csv(data, path.with_name(f"{stem}.csv"))
        print(f"  wrote {stem}.qti.zip ({n} questions) and {stem}.csv")


if __name__ == "__main__":
    main(sys.argv[1:])
