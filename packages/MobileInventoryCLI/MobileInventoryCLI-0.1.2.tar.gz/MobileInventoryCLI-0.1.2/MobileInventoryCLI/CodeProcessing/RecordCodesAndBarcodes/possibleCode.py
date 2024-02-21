import upcean
from barcode import UPCA
from colored import Fore,Style,Back

class PossibleCodes:
    def __init__(self,scanned):
        try:
            isUPC=True
            if len(scanned) > 8:
                if len(scanned) < 11:
                    scanned=scanned.zfill(11)
                elif len(scanned) == 13:
                    #scanned=scanned[(11-len(scanned)):len(scanned)]
                    scanned=scanned[len(scanned)-11:len(scanned)]
                 
                upca=UPCA(scanned)
                upcas=str(upca)
                upce=upcean.convert.convert_barcode_from_upca_to_upce(str(upca))
                upca_stripped=str(upca)
                upcas=upca_stripped
                upca_ean2=upcean.convert.convert_barcode_from_upca_to_ean13(upcas)
                upca_stripped=str(int(upca_stripped))
                upca_stripped=upca_stripped[:-1]
                print(
            f"""
{Fore.tan}{Style.underline}Telethon Code #:{Style.reset} -> {Fore.pale_green_1b}{Style.bold}{upcas[0:-1]}{Style.reset}
{Fore.cyan}UPCA -> {upca}{Style.reset}
{Fore.green}{Style.underline}UPCA Stripped{Style.reset} -> {Fore.magenta}{Style.bold}{upca_stripped}{Style.reset}
{Fore.dark_goldenrod}{Style.underline}UPCE{Style.reset} -> {Fore.magenta}{Style.bold}{upce}{Style.reset}

                   """)
            else:
                upca=upcean.convert.convert_barcode_from_upce_to_upca(scanned)
                if upca:
                    upca=UPCA(upca)
                    upcas=str(upca)
                    upca_stripped=str(upca) 
                    upca_stripped=str(int(upca_stripped)) 
                    upca_stripped=upca_stripped[:-1]

                    print(f"""
{Fore.tan}{Style.underline}Telethon Code #:{Style.reset} -> {Fore.pale_green_1b}{Style.bold}{upcas[0:-1]}{Style.reset}
{Fore.green_yellow}UPCA-Checked -> {upca}{Style.reset}
{Fore.green}{Style.underline}UPCA Stripped{Style.reset} ->{Fore.magenta}{Style.bold}{upca_stripped}{Style.reset}""")

                print(f"""
{Fore.cyan}UPCA -> {upca}{Style.reset}
{Fore.yellow}{Style.underline}UPCE{Style.reset} ->{Fore.magenta}{Style.bold}{scanned}{Style.reset}
                """)
            print(f"{Fore.yellow}PickList Code -> {str(str(upca)[:-1]).zfill(13)}{Style.reset}")
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
            try:
                PossibleCodes(scanned=code)
            except Exception as e:
                print(str(e))
                print(repr(e))
