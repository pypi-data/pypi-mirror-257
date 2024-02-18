import upcean
from barcode import UPCA
from colored import Fore,Style,Back

class PossibleCodes:
    def __init__(self,scanned):
        try:
            if len(scanned) > 8:
                if len(scanned) < 11:
                    scanned=scanned.zfill(11)
                upca=UPCA(scanned)
                upca_ean=UPCA(scanned,make_ean=True)
                upce=upcean.convert.convert_barcode_from_upca_to_upce(str(upca))
                upca_stripped=str(upca) 
                upca_stripped=str(int(upca_stripped))
                upca_stripped=upca_stripped[:-1]
                print(
            f"""
{Fore.cyan}UPCA -> {upca}{Style.reset}
{Fore.green}{Style.underline}UPCA Stripped{Style.reset} -> {Fore.magenta}{Style.bold}{upca_stripped}{Style.reset}
{Fore.red}UPCA_EAN -> {upca_ean}{Style.reset}
{Fore.dark_goldenrod}{Style.underline}UPCE{Style.reset} -> {Fore.magenta}{Style.bold}{upce}{Style.reset}

                   """)
            else:
                upca=upcean.convert.convert_barcode_from_upce_to_upca(scanned)
                if upca:
                    upca_ean=UPCA(upca,make_ean=True)
                    upca=UPCA(upca)
                    upca_stripped=str(upca) 
                    upca_stripped=str(int(upca_stripped)) 
                    upca_stripped=upca_stripped[:-1]

                    print(f"""{Fore.red}UPCA_EAN -> {upca_ean}{Style.reset}
{Fore.green_yellow}UPCA-Checked -> {upca}{Style.reset}
{Fore.green}{Style.underline}UPCA Stripped{Style.reset} ->{Fore.magenta}{Style.bold}{upca_stripped}{Style.reset}""")

                print(f"""
{Fore.cyan}UPCA -> {upca}{Style.reset}
{Fore.yellow}{Style.underline}UPCE{Style.reset} ->{Fore.magenta}{Style.bold}{scanned}{Style.reset}

                """)

        except Exception as e:
            print(e)
if __name__ == "__main__":
    PossibleCodes(scanned=input("code"))


def run():
    while True:
        code=input("code: ")
        if code.lower() in ['q','quit']:
            exit()
        else:
            PossibleCodes(scanned=code)
