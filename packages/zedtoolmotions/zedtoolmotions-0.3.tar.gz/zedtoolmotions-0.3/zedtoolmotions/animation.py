import time
import colorama

class Animation:
    def __init__(self):
        pass

    def animate(self,speed):
        text = f"""
{colorama.Fore.RESET}-----------------------------------------------------------------------
{colorama.Fore.LIGHTGREEN_EX}                                       ████████████████████████████████               
                                       ████████████████████████████████               
  ███                                  ████████████████████████████████               
  █████                                ████████████████████████████████               
   ██████                              ████             █             █               
     █████                             ███             █              █               
       █████                           ██████████     ███████    ██████               
         █████                         █████████    █████████    ██████               
          █████                        ███████     █████████     ██████               
        █████                          ██████     ██████████    ███████               
      ██████                           █████    ████████████    ███████               
     █████                             ███     █████████████    ███████               
   █████                               ██             █████     ███████               
 █████                                 █              █████     ███████               
████             █████████████████     ████████████████████████████████               
                 █████████████████     ████████████████████████████████               
                 █████████████████     ████████████████████████████████               
                                       ████████████████████████████████               
{colorama.Fore.RESET}-----------------------------------------------------------------------
{colorama.Fore.RED}╦ ╦┌─┐┬ ┬┌─┐┌─┐┌─┐┬┌─┐  ╔╦╗┬ ┬┬ ┬┌─┐┌┬┐┌┬┐┌─┐┌┬┐
╚╦╝│ ││ │└─┐└─┐├┤ │├┤   ║║║│ │├─┤├─┤││││││├┤  ││
 ╩ └─┘└─┘└─┘└─┘└─┘┴└    ╩ ╩└─┘┴ ┴┴ ┴┴ ┴┴ ┴└─┘─┴┘
{colorama.Fore.RESET}-----------------------------------------------------------------------
{colorama.Fore.LIGHTRED_EX}[$] Developed By {colorama.Fore.RESET}" {colorama.Fore.GREEN}Yousseif Muhammed {colorama.Fore.RESET}"
{colorama.Fore.LIGHTYELLOW_EX}[$] Telegram Account & Channel: {colorama.Fore.RESET}({colorama.Fore.GREEN} @YousseifMuhammed {colorama.Fore.RESET}| {colorama.Fore.GREEN}@ZEDTOOL {colorama.Fore.RESET})
{colorama.Fore.CYAN}[$] Don't Change Rights, you donkey ;<)
{colorama.Fore.RESET}-----------------------------------------------------------------------
"""

        for char in text:
            print(char, end='', flush=True)
            time.sleep(speed)  # Adjust the delay as needed
