"""

  _      _ _                    _           
 | |    (_) |                  (_)          
 | |     _| |__  _ __ __ _ _ __ _  ___  ___ 
 | |    | | '_ \| '__/ _` | '__| |/ _ \/ __|
 | |____| | |_) | | | (_| | |  | |  __/\__ \
 |______|_|_.__/|_|  \__,_|_|  |_|\___||___/
                                            
                                            

"""

import signal
import msvcrt
import time
import base64

"""

   _____          _                    _                   _   
  / ____|        | |                  (_)                 | |  
 | |    _   _ ___| |_ ___  _ __ ___    _ _ __  _ __  _   _| |_ 
 | |   | | | / __| __/ _ \| '_ ` _ \  | | '_ \| '_ \| | | | __|
 | |___| |_| \__ \ || (_) | | | | | | | | | | | |_) | |_| | |_ 
  \_____\__,_|___/\__\___/|_| |_| |_| |_|_| |_| .__/ \__,_|\__|
                                              | |              
                                              |_|              

"""
usersystems = input("If you are on linux, enter 1, if you are on windows, enter 2.")
if usersystems == "1":
    def timeout_handler(signum, frame):
        print("\nNo choice chosen")  # Message when timeout occurs
        raise EOFError  # Exit the input without raising an exception

    def Input(prompt, timeout, exitval):
        # Set the timeout handler
        signal.signal(signal.SIGALRM, timeout_handler)
        # Schedule the timeout signal
        signal.alarm(timeout)

        try:
            # Try to get input
            user_input = input(prompt)
            signal.alarm(0)  # Cancel the alarm if input is successful
            return user_input
        except EOFError:
            # If timeout occurs, just return None without raising an exception
            return exitval

else:
    def Input(prompt, timeout,exitval):
        print(prompt, end='', flush=True)
        start_time = time.time()
        input_string = ''

        while True:
            # Check if input is available
            if msvcrt.kbhit():
                char = msvcrt.getche()  # Get character and echo it to the console
                if char == b'\r':  # Enter key pressed
                    print()  # Move to a new line after input
                    break
                else:
                    input_string += char.decode("utf-8")
        
        # Check if timeout has been reached
            if time.time() - start_time > timeout:
                return exitval
        
        time.sleep(0.1)  # Small delay to prevent high CPU usage
    
        return input_string

"""

   ____        _ 
  / __ \      | |
 | |  | | ___ | |
 | |  | |/ _ \| |
 | |__| | (_) | |
  \___\_\\___/|_|
                 
                 

"""

def encode64(sample_string):
    sample_string_bytes = sample_string.encode("ascii")

        # Encode the bytes to Base64
    base64_bytes = base64.b64encode(sample_string_bytes)

    # Convert the Base64 bytes back to a string
    base64_string = base64_bytes.decode("ascii")
    return(base64_string)

def decode_base64(input_string,errormessage):
    try:
        # Add padding if necessary
        input_string = input_string.strip()
        missing_padding = len(input_string) % 4
        if missing_padding:
            input_string += '=' * (4 - missing_padding)
        
        # Decode the input
        decoded_bytes = base64.b64decode(input_string)
        return decoded_bytes.decode('utf-8')
    except base64.binascii.Error:
        return(errormessage)
    except UnicodeDecodeError:
        return(errormessage)

def eform(x):
    if x > 999:
        zeros = 0
        for i in str(x):
            if i == ".":
                return(eform(int(x)))
            else:
                zeros +=1
        return(f"{str(x/10**(zeros-1))[:3:]}e{zeros}")
    return(int(x))        


def intabove(x,minim,exitmenumessage,exitprompt):
   if x == exitprompt:
       return(exitprompt)
   n = x
   while not type(n) == int:
        try:
            int(n)
        except ValueError:
            if x == exitprompt:
                return(exitprompt)
            print(f"Error, {n} is not a whole number:")
            n = Input(f"Please enter a whole number above or equal to {minim}. {exitmenumessage}\n",input_time,exitprompt)
        else:
            if n == exitprompt:
                return(exitprompt)
            if int(n) >= minim:
                x = int(n)
                return(x)
            else:
                return(intabove(Input(f"Error, {n} is not a whole:\nPlease enter a whole number above or equal to {minim}. {exitmenumessage}\n",input_time,exitprompt),minim))

def genprice(gen,price,bought,buying): #Calculate how much buying an amount of a gen will cost
    genpricejump = {1:10**3,2:10**4,3:10**5,4:10**6,5:10**8,6:10**10,7:10**12,8:10**15}#every 10 bought multiply the gen price by:
    till10 = 10 - bought % 10
    temp = min([till10,buying])
    bought += temp
    fullprice =  temp * price
    buyingtemp = buying - temp
    if temp <= buying:
        price *= genpricejump[gen]
        for i in range ((buyingtemp)//10):
            fullprice += 10*price
            buyingtemp -= 10
            price *= genpricejump[gen]
        buying = buyingtemp
        bought += 10*(buyingtemp-bought)//10
        fullprice += (buying)*price
    return([fullprice,price])



"""

  __  __                  
 |  \/  |                 
 | \  / | ___ _ __  _   _ 
 | |\/| |/ _ \ '_ \| | | |
 | |  | |  __/ | | | |_| |
 |_|  |_|\___|_| |_|\__,_|
                          
                          

"""

def stopmenu(): #stopmenu
    running = Input("If you want to continue playing, enter 1, else enter 0.\n",input_time,1)
    while not running in [0,1]: #Making sure the input is valid
        try:
            int(running)
        except ValueError:#Fixing it if it is not
            print(f"\nError, {running} is neither 1 or 0")
            running = Input("If you want to continue, enter 1, else enter 0.\n",input_time,1)
        else:
            running = int(running)
    return(running)
            
    

def upgrademenu(gens,updaterate,score,tickspeed): #Upgrade menu
    print(f"\nYour sps (Score Per Second) is {gens[0][0]* tickspeed[0]}")
    for i in reversed(gens[:-1:]): #Printing the info for the player
        if gens.index(i) == 0:#Printing the gain per second
            print(f"Your have {eform(i[0])} tier 1 generators, generating {eform(i[0]*tickspeed[0])} score per second. One upgrade will cost {eform(i[1])}.")
        else:#Printing the upgrade info
            print(f"Your have {eform(i[0])} tier {gens.index(i)+1} generator, generating {eform(i[0]*tickspeed[0])} of tier {gens.index(i)} gens per second. One upgrade will cost {eform(i[1])}")
    print(f"Your tickspeed is {eform(tickspeed[0])} which means you gain {eform(tickspeed[0])} times more score and gens per a second (included in the calculations above.)")
    gen = Input("\nWhich gen do you want to upgrade? If you want to upgrade tickspeed, enter 9, and if you want to exit this menu enter 0.\n",input_time,0)
    if gen == "0":
        return(gens,score,tickspeed)
    while not type(gen) == int:#making sure the gen is a gen
        try:
            test = gens[int(gen)-1]
        except IndexError:
            print(f"Error, {gen} is not a valid upgrade:")
            gen = Input("Please enter the number of the gen you want to upgrade. If you want to upgrade tickspeed , enter 9, and to exit this menu enter 0.\n",input_time,0)
        except ValueError:
            print(f"Error, {gen} is not a valid upgrade:")
            gen = Input("Please enter the number of the gen you want to upgrade. If you want to upgrade tickspeed , enter 9, and to exit this menu enter 0.\n",input_time,0)
        else:
            if int(gen) == 0:
                return(gens,score,tickspeed)
            elif int(gen) == 9:
                bought = (f"How many tickspeed upgrades would you like to buy? Each upgrade multiplies the cost by 10 and the tickspeed by 1.125, and your current price for one upgrade is {tickspeed[1]}")
                if bought == "0":#If the player does not want to buy a gen go back
                    return(upgrademenu((gens,updaterate,score)))
                print("bruh why am i here")
                bought = intabove(bought,0,"Enter 0 to exit this menu","0")
                if bought == "0":
                    print("Menu exited")
                    return(gens,score,tickspeed)
                else:
                    price = tickspeed[1]
                    fullprice = 0
                    for i in range(bought): #getting the purchase info
                        fullprice += price ** (i+1)
                    price *= bought
                    priceinfo = [fullprice,price]
                    if priceinfo[0] > score:#checking the player balance
                        print(f"Womp Womp, you are too poor to buy this by {eform(priceinfo[0] - score)} points")
                    else:
                        confirm = Input(f"Are you sure you want to buy {eform(bought)} tickspeed upgrades, costing {eform(priceinfo[0])} points. \nEnter Y or y for confirmation, anything else to cancel.\n",input_time,0).lower()
                        if confirm != "y":
                            print("Purchase canceled: Exiting this menu...")
                        else:
                            score -= priceinfo[0]
                            tickspeed[0] *= (1.125**bought)
                            tickspeed[1] == priceinfo[1]
                            tickspeed[2] += bought
                            print(f"Bought {eform(bought)} tickspeed upgrades.")
            elif int(gen) in [1,2,3,4,5,6,7,8]:
                gen = int(gen)
    bought = Input("\nHow much would you like to upgrade this gen? If you want to exit this menu enter 0.\n",input_time,0)
    if bought == "0":#If the player does not want to buy a gen go back
        return(upgrademenu((gens,updaterate,score)))
    bought = intabove(bought,0,"Enter 0 to exit this menu","0")
    if bought == "0":
        print("Menu exited")
        return(gens,score,tickspeed)
    else:
        priceinfo = genprice(gen,gens[gen-1][1],gens[gen-1][2],bought) #getting the purchase info
        if priceinfo[0] > score:#checking the player balance
            print(f"Womp Womp, you are too poor to buy this by {eform(priceinfo[0] - score)} points")
        else:
            confirm = Input(f"Are you sure you want to buy {eform(bought)} tier {gen} gens, costing {eform(priceinfo[0])} points. \nEnter Y or y for confirmation, anything else to cancel.\n",input_time,0).lower()
            if confirm != "y":
                print("Purchase canceled: Exiting this menu...")
            else:
                score -= priceinfo[0]
                gens[gen-1][0] += bought
                gens[gen-1][1] = priceinfo[1]
                gens[gen-1][2] += bought
                gens[gen-1][3] = 2 ** (gens[gen-1][2]//10)
                print(f"Bought {eform(bought)} of gen {gen}")
    return(gens,score,tickspeed)


def settings(updaterate,action,input_time):#settings menu
    if updaterate > 1:
        ups = f"every {updaterate} seconds"
    else:
        ups = f"{1/updaterate} times a second"
    print(f"The game currently: Updating the screen (Showing you your score), letting you choose an action every {action} seconds and your input time (time to enter your choices for menus) is {input_time} seconds. It is strongly reccomended to leave input time above 3 seconds, and smallest allowed value is 1 second.")
    choice = Input("Which setting would you like to change? Enter it's number or exit to exit: \n 1. Update rate\n 2. Action rate\n 3. Input time \nChoose which one you want to change or enter exit to exit settings menu.\n",input_time,"exit")
    if choice == "2": #choosing the setting to change
        actionrate = Input("Please input the interval in seconds you want for the actions. Default is 10 seconds per action.\n",input_time,action)
        while type(actionrate) != float: #Making sure the input is valid
            try:
                float(actionrate)
            except ValueError:#Fixing it if it is not
                print(f"\nError, {actionrate} is not a number")
                actionrate = Input("Please input the interval in seconds you want for the actions. Default is 10 seconds per action.\n",input_time,action)
            else:
                print(f"Changed action rate from {action} seconds to {actionrate} seconds between actions")
                actionrate = float(actionrate)
                action = actionrate
    elif choice == "1": #choosing the setting to change
        update = Input("Please input the interval in seconds you want for the updates per seconds. Default is 1 second per update.\n",input_time,updaterate)
        while type(update) != float: #Making sure the input is valid
            try:
                float(update)
            except ValueError:#Fixing it if it is not
                print(f"\nError, {update} is not a number")
                update = Input("Please input the interval in seconds you want for the actions. Default is 1 second per update.\n",input_time,updaterate)
            else:
                print(f"Changed update rate from {updaterate} seconds to {update} seconds per update")
                update = float(update)
                updaterate = update
    elif choice == "3": #choosing the setting to change
        inputtime = Input("Please input the amount of seconds you want to be able to type answers to prompts like this one. Notice you can only input whole numbers above 1. It is strongly reccomended to keep this setting above 3 seconds.\n",input_time,input_time)
        inputtime = intabove(inputtime,1,"Enter 0 to exit this menu","0")
        if inputtime == "0":
            print("No settings changed")
            return[updaterate,action,input_time]
        print(f"Changed input time from {input_time} seconds to {inputtime} seconds to choose")
        inputtime = int(inputtime)
        input_time = inputtime
    else:
        print("No settings changed")
    return[updaterate,action,input_time]
            

"""

   _____      _   _   _                             _   _                                       
  / ____|    | | | | (_)                           | | | |                                      
 | (___   ___| |_| |_ _ _ __   __ _   _   _ _ __   | |_| |__   ___    __ _  __ _ _ __ ___   ___ 
  \___ \ / _ \ __| __| | '_ \ / _` | | | | | '_ \  | __| '_ \ / _ \  / _` |/ _` | '_ ` _ \ / _ \
  ____) |  __/ |_| |_| | | | | (_| | | |_| | |_) | | |_| | | |  __/ | (_| | (_| | | | | | |  __/
 |_____/ \___|\__|\__|_|_| |_|\__, |  \__,_| .__/   \__|_| |_|\___|  \__, |\__,_|_| |_| |_|\___|
                               __/ |       | |                        __/ |                     
                              |___/        |_|                       |___/                      

"""


#setting up the code for the loop
input_time = 10
gens = [[1,10,1,1],[0,100,0,1],[0,10**4,0,1],[0,10**6,0,1],[0,10**9,0,1],[0,10**13,0,1],[0,10**18,0,1],[0,10**24,0,1],9]
updaterate = 1
secs = 0
score = 0
running = 1
action = 10
actionrate = 10
tickspeed = [1,1000,0]
"""

  _____                            _                                
 |_   _|                          | |                               
   | |  _ __ ___  _ __   ___  _ __| |_    __ _  __ _ _ __ ___   ___ 
   | | | '_ ` _ \| '_ \ / _ \| '__| __|  / _` |/ _` | '_ ` _ \ / _ \
  _| |_| | | | | | |_) | (_) | |  | |_  | (_| | (_| | | | | | |  __/
 |_____|_| |_| |_| .__/ \___/|_|   \__|  \__, |\__,_|_| |_| |_|\___|
                 | |                      __/ |                     
                 |_|                     |___/                      

"""
save_format = [score,tickspeed[0],tickspeed[1],tickspeed[2],gens[0][0],gens[0][1],gens[0][2],gens[0][3],gens[1][0],gens[1][1],gens[1][2],gens[1][3],gens[2][0],gens[2][1],gens[2][2],gens[2][3],gens[3][0],gens[3][1],gens[3][2],gens[3][3],gens[4][0],gens[4][1],gens[4][2],gens[4][3],gens[5][0],gens[5][1],gens[5][2],gens[5][3],gens[6][0],gens[6][1],gens[6][2],gens[6][3],gens[7][0],gens[7][1],gens[7][2],gens[7][3],secs,updaterate,action,actionrate,input_time]
save = Input("Do you have a save? If so, enter yes, otherwise enter anything else: \n",15,"no")
worked= True
if save == "yes":
    worked = False
while not worked:
    save = Input("Please enter your save, if you don't have a save or don't want to use the save, enter 0: \n",15,"0")
    if save == "0":
        break
    else:
        saved = save.split(",")
        save = []
        for i in saved:
            if decode_base64(i,"Invalid save... are you trying to cheat😤😤😤?") == "Invalid save... are you trying to cheat😤😤😤?":
                print("Invalid save... are you trying to cheat😤😤😤1?")
                running = 0
                break
            else:
                save.append(decode_base64(i,"invalid"))
        worked = True
    if len(save_format) < len(save):
        print("Invalid save... are you trying to cheat😤😤😤2?")
        running = 0
    else:
        goodsave = True
        for i in range(len(save)):
            try:
                save[i] = int(save[i])
            except ValueError:
                try:
                    save[i] = float(save[i])
                except ValueError:
                    print("Invalid save... are you trying to cheat😤😤😤3?")
                    goodsave = False
                    break
        if goodsave:
            score = save[0]
            tickspeed = [save[1],save[2],save[3]]
            gens = [[save[4],save[5],save[6],save[7]],[save[8],save[9],save[10],save[11]],[save[12],save[13],save[14],save[15]],[save[16],save[17],save[18],save[19]],[save[20],save[21],save[22],save[23]],[save[24],save[25],save[26],save[27]],[save[28],save[29],save[30],save[31]],[save[32],save[33],save[34],save[35]],9]
            secs = save[36]
            updaterate = save[37]
            action = save[38]
            actionrate = save[39]
            input_time = save[40]

"""

  _______ _                                          __                                             _    
 |__   __| |                                        / _|                                           | |   
    | |  | |__   ___    __ _  __ _ _ __ ___   ___  | |_ _ __ __ _ _ __ ___   _____      _____  _ __| | __
    | |  | '_ \ / _ \  / _` |/ _` | '_ ` _ \ / _ \ |  _| '__/ _` | '_ ` _ \ / _ \ \ /\ / / _ \| '__| |/ /
    | |  | | | |  __/ | (_| | (_| | | | | | |  __/ | | | | | (_| | | | | | |  __/\ V  V / (_) | |  |   < 
    |_|  |_| |_|\___|  \__, |\__,_|_| |_| |_|\___| |_| |_|  \__,_|_| |_| |_|\___| \_/\_/ \___/|_|  |_|\_\
                        __/ |                                                                            
                       |___/                                                                             

"""
while running == 1:
    time.sleep(updaterate)#updating on the speed the player wants
    secs += updaterate 
    action -= updaterate
    for i in gens[:-2:]:
        i[0] += gens[gens.index(i)+1][0] * updaterate * tickspeed[0]
    score += gens[0][0] * updaterate * tickspeed[0]
    print(f"Your current score is {score}")
    if action <= 0:
        print(f"\nChoose which menu to go to:\n 1. Stop menu\n 2. Upgrade menu\n 3. Settings menu\n 4. Import/Export game menu\n Notice that you can only do the next action in {actionrate} seconds, which can be change via settings")
        menuchoice = Input("Choose the number of the menu you want to go to:\n",input_time,0) #giving the player a chance to upgrade and or stop
        if menuchoice == "1":
            runnnig = stopmenu()
        elif menuchoice == "2":
            upgrades = upgrademenu(gens,updaterate,score,tickspeed)
            gens = upgrades[0]
            score = upgrades[1]
            tickspeed = upgrades[2]
        elif menuchoice == "3":
            setting = settings(updaterate, actionrate,input_time)
            updaterate = setting[0]
            actionrate = setting[1]
            input_time = setting[2]
        elif menuchoice == "4":
            export_or_import = Input("Would you like to import or export your save?\nEnter 1 to export, 2 to import or 0 to cancel:\n",input_time,"0")
            if not export_or_import == "0":
                if export_or_import == "1":
                    saving_format = [score,tickspeed[0],tickspeed[1],tickspeed[2],gens[0][0],gens[0][1],gens[0][2],gens[0][3],gens[1][0],gens[1][1],gens[1][2],gens[1][3],gens[2][0],gens[2][1],gens[2][2],gens[2][3],gens[3][0],gens[3][1],gens[3][2],gens[3][3],gens[4][0],gens[4][1],gens[4][2],gens[4][3],gens[5][0],gens[5][1],gens[5][2],gens[5][3],gens[6][0],gens[6][1],gens[6][2],gens[6][3],gens[7][0],gens[7][1],gens[7][2],gens[7][3],secs,updaterate,action,actionrate,input_time]  
                    save = ""
                    for i in saving_format:
                        save += encode64(str(i)) + ","
                    print("The following code can be inputted either in the import option or in the start when the game asks if you have a save to get back to your current state of the game.")
                    print(save[:-1:])
                    print("The game will wait 10 seconds to let you copy the save code.")
                    time.sleep(10)
                elif export_or_import == "2":
                    save = Input("Do you have a save? If so, enter yes, otherwise enter anything else: \n",15,"no")
                    worked= True
                    if save == "yes":
                        worked = False
                    while not worked:
                        save = Input("Please enter your save, if you don't have a save or don't want to use the save, enter 0: \n",15,"0")
                        if save == "0":
                            break
                        else:
                            saved = save.split(",")
                            save = []
                            for i in saved:
                                if decode_base64(i,"Invalid save... are you trying to cheat😤😤😤?") == "Invalid save... are you trying to cheat😤😤😤?":
                                    print("Invalid save... are you trying to cheat😤😤😤?")
                                    break
                                else:
                                    save.append(decode_base64(i,"invalid"))
                            worked = True
                        if len(save_format) < len(save):
                            print("Invalid save... are you trying to cheat😤😤😤?")
                        else:
                            goodsave = True
                            for i in range(len(save)):
                                try:
                                    save[i] = int(save[i])
                                except ValueError:
                                    try:
                                        save[i] = float(save[i])
                                    except ValueError:
                                        print("Invalid save... are you trying to cheat😤😤😤?")
                                        goodsave = False
                                        break
                            if goodsave:
                                score = save[0]
                                tickspeed = [save[1],save[2],save[3]]
                                gens = [[save[4],save[5],save[6],save[7]],[save[8],save[9],save[10],save[11]],[save[12],save[13],save[14],save[15]],[save[16],save[17],save[18],save[19]],[save[20],save[21],save[22],save[23]],[save[24],save[25],save[26],save[27]],[save[28],save[29],save[30],save[31]],[save[32],save[33],save[34],save[35]],9]
                                secs = save[36]
                                updaterate = save[37]
                                action = save[38]
                                actionrate = save[39]
                                input_time = save[40]
        else:
            print(f"No action was taken, Next action in {actionrate} seconds")
        action = actionrate


