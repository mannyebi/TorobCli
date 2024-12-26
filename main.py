#1- get the user's desired search on torob
#2- send request to that specific url 
#3- get the data and do what ever you want with it

#to redirect user to web browser. use this -> import webbrowser \n webbrowser.open("link")
import curses
import api
import sys
import webbrowser
from storing import add_record


current_column = 1
current_row = 1
product_context = None
current_page = 1
search_query = None
search_size = 10

def start_color():
    """starting colors and color configs.
    """
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)  # Red text
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)  # Green text
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)  # Blue text
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Blue text
    curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Blue text



def welcome_message(stdscr, start_line):
    """display a starter welcome message for user.
    Args:
        stdscr: ...
        start_line(int): the "y" cordinate of your desired line to start
    """
    stdscr.clear() #clear everything before displaying the message.
    stdscr.addstr(start_line, 0, "input your desired product's name (press 'q' to exit!) : ")


def get_user_input(stdscr, start_line):
    """get a string from user and return it.

    Args:
        stdscr: default value for displaying message.
        start_line(int): the "y" cordinate of your desired line to start
    """
    start_color() # first of all start the colors configuration.
    stdscr.addstr(start_line, 0, "> ", curses.color_pair(4))
    curses.echo()
    command = stdscr.getstr(start_line, 3, 40).decode("utf-8")
    return command



def commands_key(key, stdscr=None):
    """return propper functions considering user's ipnuted command.
    Args:
        key(char): what user inputed.
    """
    global current_column
    global current_row
    global current_page

    if key == ord('q') or key == ord("ض"):
        sys.exit()
    elif key == curses.KEY_UP:
        current_column -= 1
    elif key == curses.KEY_DOWN:
        current_column += 1
    elif key == curses.KEY_ENTER or key in [10, 13]:
        product_action(stdscr)
    elif key == ord("z") or key == ord("ظ"):
        if product_context: #check if product_context has any data in it. if yes, return user to query pages
            show_search_result(stdscr, products=product_context)
    elif key == ord("r") or key == ord("ق"):
        if product_context:
            redirect(product_context['products'][current_column][2])
    elif key == curses.KEY_LEFT:
        if current_row > 1:
            current_row -= 1
    elif key == curses.KEY_RIGHT:
        if current_row <2:
            current_row += 1
    elif key == ord("m") or key == ord("ئ"):
        current_page += 1
        show_search_result(stdscr, query=search_query, search_size=search_size, page=current_page)
    elif key == ord("n") or key == ord("د"):
        if current_page > 1 :
            current_page -= 1
            show_search_result(stdscr, search_query, search_size, page=current_page)



def check_column_limits(max):
    """check if column limits are true or not. if not, fix it.

    Args:
        max(int): the maximum number of the column.
    """
    global current_column
    if current_column > max:
        current_column = max
    elif current_column < 1 :
        current_column = 1


def check_row_limits(max):
    """check if row limits are true or not. if not, fix it.

    Args:
        max(int): the maximum number of the column.
    """
    global current_row
    if current_row > max:
        current_row = max
    elif current_row < 1 :
        current_row = 1



def show_search_result(stdscr=None, query=None, search_size=None, products=None, page=1):
    """show the result of api request. 

    Args:
        stdscr: -.
        query(str): the product you wanna search.
        search_size(int): the number of products you wanna get.
    """
    global product_context #to make this variable global, so all functions can access it if it's not None
    global search_query

    start_color()
    if products is None:
        product_context = api.send_request(query, search_size, page)
    if query :
        search_query = query
    stdscr.clear() #clear the page before showing
    while True:
        stdscr.refresh()
        product_count = product_context["count"]
        if products is None: #show this line if it is the first time searching and not a returned one from product action page.
            stdscr.addstr(0, 0, f"first {search_size} results for -- {query} -- count {product_count}")
        #show the products and their prices
        stdscr.refresh()
        for index, product in enumerate(product_context['products'], start=1):
            if current_column == index:
                stdscr.addstr(index, 0, f"> {product[0]}", curses.color_pair(4)) #product[0] is the product's name
            else:
                stdscr.addstr(index, 0, f"> {product[0]}")
        #get key for future changes. weather exiting or ...
        stdscr.addstr(len(product_context['products'])+2, 0, f"current page : {current_page}  | press 'm' to go to next page, press 'n' to go to previous page.", curses.color_pair(5))
        key = stdscr.getch()
        commands_key(key, stdscr)
        check_column_limits(len(product_context['products']))
        


def product_action(stdscr):
    """show the detail for a specific product.

    Args:
        stdscr(-):
    """
    column = current_column
    product = product_context["products"]
    product_name = product[column - 1][0]
    product_price = humanize(product[column - 1][1]) #[1] is for product's price
    product_link = product[column-1][2] #product link


    if product_context and stdscr:
        while True:
            product = product_context

            stdscr.clear()
            start_color()
            stdscr.addstr(0, 0, "Press 'z' to return. press 'h' to save. ", curses.color_pair(2)) #help text
            stdscr.addstr(1, 0, "The Product: ", curses.color_pair(4))
            stdscr.addstr(2, 0, product_name)
            stdscr.addstr(3, 0, "Price in Toman: ", curses.color_pair(4))
            stdscr.addstr(4, 0, product_price)
            horzintal_menu(stdscr, 5)
            key = stdscr.getch()
            if key == curses.KEY_ENTER or key in [10, 13]:
                if current_row == 1:
                    add_record(product_name, product_price, product_link)
                    if product_context: #check if product_context has any data in it. if yes, return user to query pages
                        show_search_result(stdscr, products=product_context)
                elif current_row == 2:#I know its a bad approach but :) this is for redirecting
                    redirect(product_link)
            commands_key(key, stdscr)



def redirect(link):
    """Redirect user to a link using web browser

    Args:
        link(str): the link you wanna redirect user to.
    """
    torob_domain = "https://torob.com"
    link = torob_domain+link
    webbrowser.open(link)



def horzintal_menu(stdscr, start_line):
    """show a horzintal menu of this actions -> save, redirect

    Args:
        stdscr(-):-
    """
    action_list = ["Save", "Redirect"]
    if product_context:
        start_color()
        for index, action in enumerate(action_list, start=1):
            if index == current_row:
                stdscr.addstr(start_line, index*5, action, curses.color_pair(5))
            else:
                stdscr.addstr(start_line, index*5, action)


def humanize(price:int):
    """return the int price into a humanized readable price by adding , to each 3 digits.

    Args:
        price(int): the prodct's price

    """
    formatted_number = f"{price:,}"
    return formatted_number





def main(stdscr):
    """main function. Where the magic happens 😉
    """
    global search_size
    while True:
        start_color()
        welcome_message(stdscr, 0)
        search_query = get_user_input(stdscr, 1)
        #show results :
        
        show_search_result(stdscr, search_query, 10)
        search_size = 10
# Run the curses application
curses.wrapper(main)
