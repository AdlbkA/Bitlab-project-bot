import telebot
import mysql.connector
from mytoken import *

mydb = mysql.connector.Connect(
    host="localhost",
    port=3306,
    user="root",
    password="",
    database="project"
)

token = tokenn
bot = telebot.TeleBot(token)

mycursor = mydb.cursor()

def read_restaurants():
    sql = "select * from restaurants"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    return result


def read_food_types():
    sql = "select * from food_types"
    mycursor.execute(sql)
    return mycursor.fetchall()


def read_foods():
    sql = "select f.name, f.price, f.description, ft.name as foodtype_id, r.name as restaurant_id " \
          "from foods f " \
          "left outer join food_types ft on ft.id = f.foodtype_id " \
          "left outer join restaurants r on r.id = f.restaurant_id "
    mycursor.execute(sql)
    result = mycursor.fetchall()
    return result





def getFoodsByRestaurantId(id):
    global mydb
    mycursor = mydb.cursor()

    sql = "SELECT f.id, f.name, f.price, f.description, f.restaurant_id, f.foodtype_id, ft.name as foodType, r.name as restaurantName " \
          "FROM foods f " \
          "LEFT OUTER JOIN food_types ft ON ft.id = f.foodtype_id " \
          "LEFT OUTER JOIN restaurants r ON r.id = f.restaurant_id " \
          "WHERE f.restaurant_id = "+str(id)
    mycursor.execute(sql)
    result = mycursor.fetchall()

    return result

def getFoodByFoodType(id):
    global mydb
    mycursor = mydb.cursor()

    sql = "SELECT f.id, f.name, f.price, f.description, f.restaurant_id, f.foodtype_id, ft.name as foodType, r.name as restaurantName " \
          "FROM foods f " \
          "LEFT OUTER JOIN food_types ft ON ft.id = f.foodtype_id " \
          "LEFT OUTER JOIN restaurants r ON r.id = f.restaurant_id " \
          "WHERE f.foodtype_id = "+str(id)
    mycursor.execute(sql)
    result = mycursor.fetchall()

    return result

def getFood(id):
    mycursor = mydb.cursor()
    sql = "SELECT f.id, f.name, f.price, f.description, r.name as restaurant_id, ft.name as foodtype_id " \
          "FROM foods f " \
          "LEFT OUTER JOIN food_types ft ON ft.id = f.foodtype_id " \
          "LEFT OUTER JOIN restaurants r ON r.id = f.restaurant_id " \
          "WHERE f.id = " + str(id)
    mycursor.execute(sql)
    result = mycursor.fetchall()

    return result


menu = "main"
cart = []
@bot.message_handler(commands=["start"])
def handle_start(message):
    global cart
    reply_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    reply_markup.row("/start", "/stop")
    reply_markup.row("start")
    reply_markup.row("1")
    reply_markup.row("2")
    bot.send_message(message.chat.id, "Здравствуйте", reply_markup=reply_markup)

@bot.message_handler(commands=["stop"])
def handle_start(message):
    remove_markup = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, "Stop", reply_markup=remove_markup)

@bot.message_handler(content_types=["text"])
def handle_text(message):

    global menu

    if message.text.lower() == "start":
        text = ""
        text = text + "#########################\n"
        text = text+ "Добро пожаловать в сервис заказа еды\n"
        text = text+ "#########################\n"
        text = text+ "Выберите опцию поиска: \n"
        text = text+ "1 - поиск по типу еды\n"
        text = text+ "2 - поиск по ресторану\n"
        text = text+ "3 - Корзина\n"
        bot.send_message(message.chat.id, text)
        menu = "main"

    else:
        if menu == "main":
            if message.text.lower() == "1":
                menu = "choose_by_food_type"
                allFoodTypes = read_food_types()
                text = "#####################\n"
                for food in allFoodTypes:
                    text = text + str(food[0]) + ") " + food[1] + "\n"
                bot.send_message(message.chat.id, text)
            elif message.text.lower() == "2":
                menu = "choose_by_restaurant"
                allRestaurants = read_restaurants()
                text = "#####################\n"
                for rest in allRestaurants:
                    text = text + str(rest[0]) + ") " + rest[1] + "\n"
                bot.send_message(message.chat.id, text)

            elif message.text.lower() == "3":
                text = ""
                for i in cart:
                    text += str(i[0]) + ") " + i[1] + " " + str(i[2]) + " KZT " + "\n"
                bot.send_message(message.chat.id, text)


        elif menu == "choose_by_food_type":
            menu = "choose_food"
            id = message.text.lower()
            foods = getFoodByFoodType(id)
            text = "#####################\n"
            for food in foods:
                text = text + str(food[0]) + ") " + food[1] + " " + str(food[2]) + " KZT - " + food[7] + "\n"
            bot.send_message(message.chat.id, text)

        elif menu == "choose_by_restaurant":
            menu = "choose_food"
            id = message.text.lower()
            foods = getFoodsByRestaurantId(id)
            text = "#####################\n"
            for food in foods:
                text = text + str(food[0]) + ") " + food[1] + " " + str(food[2]) + " KZT - " + food[6] + "\n"
            bot.send_message(message.chat.id, text)

        elif menu == "choose_food":
            id = message.text.lower()
            food = getFood(id)
            cart.append(food[0])
            text = "Продукт добавлен в корзину"
            bot.send_message(message.chat.id, text)
            text = ""
            text = text + "#########################\n"
            text = text + "Добро пожаловать в сервис заказа еды\n"
            text = text + "#########################\n"
            text = text + "Выберите опцию поиска: \n"
            text = text + "1 - поиск по типу еды\n"
            text = text + "2 - поиск по ресторану\n"
            text = text + "3 - Корзина\n"
            bot.send_message(message.chat.id, text)
            menu = "main"


bot.polling(none_stop=True, interval=0)