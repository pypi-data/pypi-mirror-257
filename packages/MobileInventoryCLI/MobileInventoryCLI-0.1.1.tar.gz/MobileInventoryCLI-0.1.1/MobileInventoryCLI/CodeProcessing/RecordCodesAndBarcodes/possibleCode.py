import upcean
from barcode import UPCA
from colored import Fore,Style,Back

class PossibleCodes:
    def __init__(self,scanned):
        try:
            if len(scanned) > 8:
                if len(scanned) >= 12:
                    isEAN13=upcean.validate.validate_checksum("ean13",upc=scanned)
                    isUPC=upcean.validate.validate_checksum("upca",upc=scanned)
                    if isEAN13 and not isUPC:
                        print(f"{Fore.grey_50}{Style.underline}{scanned}{Style.reset} -> is EAN13!")

                        sc0=upcean.convert.convert_barcode_from_ean13_to_upca(scanned)
                        if not sc0:
                            raise Exception(f"Code Could not be converted to UPCA! {sc0}")
                        else:
                            scanned=sc0
                if len(scanned) < 11:
                    scanned=scanned.zfill(11)
                upca=UPCA(scanned)
                upca_ean=UPCA(scanned,make_ean=True)
                if not isUPC:
                    upce=f"Scanned Code is not UPCA! EAN13={isEAN13} UPC={scanned}"
                else:
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
                isEan8=upcean.validate.validate_checksum('ean8',upc=scanned)
                isUPCA=upcean.validate.validate_checksum("upce",upc=scanned)
                if isEan8 and not isUPCA:
                    print(f"{Fore.grey_50}{Style.underline}{scanned}{Style.reset} -> is EAN8!")
                    sc0=upcean.convert.convert_barcode_from_ean8_to_upca(scanned)
                    if sc0:
                        upca=str(UPCA(sc0))
                        upce=upcean.convert.convert_barcode_from_upca_to_upce(upca)
                        print(f"{Fore.grey_50}A Rarity! {Style.bold}upca({sc0}){Style.reset}{Fore.grey_50} was converted and is {Style.bold}UPCA({upca}){Style.reset}{Fore.grey_50}, and the attempt to convert to {Style.bold}UPCE({upce}).{Style.reset}.")


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
            try:
                PossibleCodes(scanned=code)
            except Exception as e:
                print(str(e))
                print(repr(e))
