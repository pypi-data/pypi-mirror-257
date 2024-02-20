import colorama,time
def Animation():
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
      time.sleep(0.001)
