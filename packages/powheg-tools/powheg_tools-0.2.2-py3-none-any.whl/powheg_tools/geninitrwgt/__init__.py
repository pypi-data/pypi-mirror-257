#!/usr/bin/env python3
import argparse


def pdfidtonummembers(pdfid):
    import lhapdf

    print("No number of members specified => trying LHAPDF")
    pdf = lhapdf.mkPDF(pdfid)
    pdfsetname = pdf.set().name
    pdfset = lhapdf.mkPDFs(pdfsetname)
    return len(pdfset)


def pdftoid(pdfname):
    if pdfname is None:
        return None
    elif pdfname.isdigit():
        return int(pdfname)
    else:
        print(f"PDF name {pdfname} is not a number => trying LHAPDF")
        import lhapdf

        pdfset = lhapdf.mkPDF(f"{pdfname}")
        return pdfset.lhapdfID


def main():
    parser = argparse.ArgumentParser(description="Generate initrwgt block for Powheg")

    # Adding optional argument with default value
    parser.add_argument("pdf", type=str, help="PDF number 1 and/or 2")
    parser.add_argument("-p1", "--pdf1", type=str, default=None, help="PDF number 1")
    parser.add_argument("-p2", "--pdf2", type=str, default=None, help="PDF number 2")
    parser.add_argument(
        "-n",
        "--nummembers",
        type=int,
        default=None,
        help="Number of members in PDF set",
    )
    parser.add_argument(
        "-s", "--scalevar", type=bool, default=True, help="Scale variations"
    )
    parser.add_argument(
        "-m", "--pdfvar", type=bool, default=True, help="PDF variations"
    )
    parser.add_argument("-o", "--output", type=str, default=None, help="Output file")

    args = parser.parse_args()

    pdf1 = pdftoid(args.pdf1)
    pdf2 = pdftoid(args.pdf2)

    if pdf1 is not None and pdf2 is not None:
        print("Only one of pdf1 and pdf2 can be set (other pdf is pdf)")
        exit(1)

    pdf = pdftoid(args.pdf)

    numMembers = args.nummembers
    if numMembers is None:
        numMembers = pdfidtonummembers(pdf)

    unc_scale = args.scalevar
    unc_pdf = args.pdfvar

    s = ""
    s += f"<initrwgt>\n"
    s += f"<weightgroup name='nominal' combine='None'>\n"
    s += f"<weight id='MUR1.0_MUF1.0_PDF{pdf}'>default</weight>\n"
    s += f"</weightgroup>\n"
    if unc_scale:
        s += f"<weightgroup name='scale_variations' combine='None'>\n"
        s += f"<weight id='MUR2.0_MUF2.0_PDF{pdf}'> renscfact=2d0 facscfact=2d0 </weight>\n"
        s += f"<weight id='MUR0.5_MUF0.5_PDF{pdf}'> renscfact=0.5d0 facscfact=0.5d0 </weight>\n"
        s += f"<weight id='MUR1.0_MUF2.0_PDF{pdf}'> renscfact=1d0 facscfact=2d0 </weight>\n"
        s += f"<weight id='MUR1.0_MUF0.5_PDF{pdf}'> renscfact=1d0 facscfact=0.5d0 </weight>\n"
        s += f"<weight id='MUR2.0_MUF1.0_PDF{pdf}'> renscfact=2d0 facscfact=1d0 </weight>\n"
        s += f"<weight id='MUR0.5_MUF1.0_PDF{pdf}'> renscfact=0.5d0 facscfact=1d0 </weight>\n"
        s += f"</weightgroup>"
    if unc_pdf:
        s += f"<weightgroup name='pdf_variations' combine='None'>\n"
        for i in range(1, numMembers):
            if pdf1 is not None and pdf2 is None:
                s += f"<weight id='MUR1.0_MUF1.0_PDF{pdf+i}'> lhapdf1={pdf1} lhapdf2={pdf+i}</weight>\n"
            elif pdf2 is not None and pdf1 is None:
                s += f"<weight id='MUR1.0_MUF1.0_PDF{pdf+i}'> lhapdf1={pdf+i} lhapdf2={pdf2}</weight>\n"
            elif pdf1 is None and pdf2 is None:
                s += f"<weight id='MUR1.0_MUF1.0_PDF{pdf+i}'> lhapdf={pdf+i}</weight>\n"
            else:
                print("FAILED")
                exit(1)

        s += f"</weightgroup>\n"
    s += f"</initrwgt>\n"

    if args.output is not None:
        with open(args.output, "w") as f:
            f.write(s)
    else:
        print()
        print(s)


if __name__ == "__main__":
    main()
