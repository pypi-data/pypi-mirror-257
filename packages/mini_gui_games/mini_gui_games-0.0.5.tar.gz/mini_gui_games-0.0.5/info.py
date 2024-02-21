from colorama import Fore, init as init_colorama

logo = """
        GGGGGGGGGGGGG                                                                               
     GGG::::::::::::G                                                                               
   GG:::::::::::::::G                                                                               
  G:::::GGGGGGGG::::G                                                                               
 G:::::G       GGGGGG  aaaaaaaaaaaaa      mmmmmmm    mmmmmmm       eeeeeeeeeeee        ssssssssss   
G:::::G                a::::::::::::a   mm:::::::m  m:::::::mm   ee::::::::::::ee    ss::::::::::s  
G:::::G                aaaaaaaaa:::::a m::::::::::mm::::::::::m e::::::eeeee:::::eess:::::::::::::s 
G:::::G    GGGGGGGGGG           a::::a m::::::::::::::::::::::me::::::e     e:::::es::::::ssss:::::s
G:::::G    G::::::::G    aaaaaaa:::::a m:::::mmm::::::mmm:::::me:::::::eeeee::::::e s:::::s  ssssss 
G:::::G    GGGGG::::G  aa::::::::::::a m::::m   m::::m   m::::me:::::::::::::::::e    s::::::s      
G:::::G        G::::G a::::aaaa::::::a m::::m   m::::m   m::::me::::::eeeeeeeeeee        s::::::s   
 G:::::G       G::::Ga::::a    a:::::a m::::m   m::::m   m::::me:::::::e           ssssss   s:::::s 
  G:::::GGGGGGGG::::Ga::::a    a:::::a m::::m   m::::m   m::::me::::::::e          s:::::ssss::::::s
   GG:::::::::::::::Ga:::::aaaa::::::a m::::m   m::::m   m::::m e::::::::eeeeeeee  s::::::::::::::s 
     GGG::::::GGG:::G a::::::::::aa:::am::::m   m::::m   m::::m  ee:::::::::::::e   s:::::::::::ss  
        GGGGGG   GGGG  aaaaaaaaaa  aaaammmmmm   mmmmmm   mmmmmm    eeeeeeeeeeeeee    sssssssssss    
"""


def info():
    init_colorama()
    print(Fore.LIGHTGREEN_EX + logo + Fore.RESET)
    print(f"{Fore.BLUE}Use commands:\n"
          f"{Fore.LIGHTGREEN_EX}hanoitower\n"
          f"tictactoe\n"
          f"snake\n"
          f"bandergoose\n"
          f"{Fore.BLUE}to launch the corresponding game")


if __name__ == '__main__':
    info()
