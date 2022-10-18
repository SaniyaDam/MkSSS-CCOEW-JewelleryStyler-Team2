#importing libraries
import streamlit as st
import mysql.connector as mysql
from PIL import Image

#python establishing connection with sql database
db = mysql.connect(
    host = "localhost",
    user = "root",
    passwd = "root123",
    database = "NorthernTrust"
)

cursor = db.cursor()

#function for inserting customer data in Customer table
def insertCustomer(c_name,c_email,c_address,c_phno):
    query="insert into Customer (c_name,c_email,c_address,c_phno) values(%s,%s,%s,%s)"
    VAL=[c_name,c_email,c_address,c_phno]
    cursor.execute(query, VAL)
    db.commit()

#function to submit review and add data in RandR table
def submitReview(c_id, p_id, comment, rating):
    query = "insert into RandR (c_id, p_id, comment, rating,r_time) values(%s,%s,%s,%s,now())"
    VAL= [c_id, p_id, comment, rating]
    cursor.execute(query,VAL)
    db.commit()

#function to update review , take new values and update in RandR
def updateReview(r_no,c_id,p_id,comment,rating):
    query = "update RandR set rating=%s, comment=%s ,r_time=now() where r_no=%s and c_id=%s and p_id=%s"
    VAL = [rating,comment,r_no,c_id,p_id]
    cursor.execute(query, VAL)
    db.commit()

#function to delete a review from RandR
def deleteReview(r_no):
    query = "delete from RandR where r_no=%s"
    VAL = [r_no]
    cursor.execute(query, VAL)
    db.commit()

#function to display product reviews (only if user is a customer)
def display(p_id):
    query = "select Customer.c_name,Product.p_name,Product.p_des,Product.p_price,RandR.comment,RandR.rating from RandR inner join Product on Product.p_id=RandR.p_id inner join Customer on Customer.c_id=RandR.c_id where Product.p_id=%s"
    VAL = [p_id]

    cursor.execute(query, VAL)

    records = cursor.fetchall()
    print(records)
    print_records = ''

    for row in records:
        st.write(print_records,"Customer name :",row[0])
        st.write(print_records, "Product Name :", row[1])
        st.write(print_records, "Product Description :", row[2])
        st.write(print_records, "Product Price :", row[3])
        st.write(print_records, "Comment :", row[4])
        st.write(print_records, "Rating:", row[5])
        st.write("                               ")
        st.write("                               ")


    db.commit()

#function to compute average rating of any product
def avgr(p_id):
    query1 = "select avg(rating) as AverageRating from RandR where p_id=%s"
    VAL1 = [p_id]
    st.write("Average rating of product:")
    cursor.execute(query1, VAL1)
    records = cursor.fetchone()
    print(records)
    print_records = " "

    for record in records:
        print_records += str(record) + '\n\r'
    st.write(print_records)
    db.commit()

#function to show price of every product
def price(p_id):
    query= "select p_price from Product where p_id=%s"
    VAL = [p_id]
    st.write("Price of product:")
    cursor.execute(query, VAL)
    records = cursor.fetchone()
    print(records)
    print_records = " "

    for record in records:
        print_records += str(record) + '\n\r'
    st.write(print_records)
    db.commit()

#function to allot customer a c_id and display it
def getcid():
    query = "select max(c_id) from Customer"
    VAL = []
    cursor.execute(query, VAL)
    records = cursor.fetchone()
    print(records)
    print_records = " "

    for record in records:
        print_records += str(record) + '\n\r'
    st.write(print_records)
    db.commit()

#function to allot customer a review id and display it for further use
def getrid():
    query = "select max(r_no) from RandR"
    VAL = []
    cursor.execute(query, VAL)
    records = cursor.fetchone()
    print(records)
    print_records = " "

    for record in records:
        print_records += str(record) + '\n\r'
    st.write(print_records)
    db.commit()

#driver code
def main():


    st.title('Welcome to the Jewellery Styler!:sparkles:')
    menu=["Buy Products","Create Profile","Submit Review","Update Review","Delete Review"]
    choice=st.sidebar.selectbox("Menu",menu)

    if choice=="Create Profile":

        st.subheader("Creating a profile will enable you  to write a customer review")
        c_name=st.text_input("Enter your name",max_chars=50)
        c_email= st.text_input("Enter email id", max_chars=50)
        c_address = st.text_input("Enter your address", max_chars=200)
        c_phno = st.text_input("Enter phone number", max_chars=11)


        if st.button("Submit your data"):
            insertCustomer(c_name, c_email, c_address, c_phno)
            st.success("Customer profile created!")
            st.write("Your customer id is:")
            getcid()

        else:
            st.error("Enter data to submit review!")

    elif choice=="Submit Review":
        st.subheader("Welcome to review Section :star::star::star::star::star:")
        st.write("Add customer details first!")
        c_id = st.text_input("Enter customer id", max_chars=50)
        #p_id = st.text_input("Enter product id", max_chars=50)
        choices=["Purple elegant necklace","All diamonds full set","Pearl necklace","Pendant necklace","Emerald studs","Gold earrings","Royal Dangling Diamond Earrings","Violet Ring","Simple Diamond ring","Sapphire ring"]
        sc = st.selectbox("Product List", choices)
        if sc=="Purple elegant necklace":
            p_id=701;
        elif sc == "All diamonds full set":
            p_id = 702;
        elif sc == "Pearl necklace":
            p_id = 703;
        elif sc == "Pendant necklace":
            p_id = 704;
        elif sc == "Emerald studs":
            p_id = 705;
        elif sc == "Gold earrings":
            p_id = 706;
        elif sc == "Royal Dangling Diamond Earrings":
            p_id = 707;
        elif sc == "Violet Ring":
            p_id = 708;
        elif sc == "Simple Diamond ring":
            p_id = 709;
        elif sc == "Sapphire ring":
            p_id = 710;


        comment = st.text_input("Enter comment", max_chars=50)
        rate_options=[0,1,2,3,4,5]
        rating = st.select_slider("Please provide product rating (0-5)",options=rate_options,value=1)


        if st.button("Submit your Review"):
            submitReview(c_id,p_id, comment, rating)
            st.success("Review submitted !!")
            st.write("Your review no is:")
            getrid()


        else:
            st.error("Please put all information")

    elif choice == "Update Review":

        r_no = st.text_input("Enter review number")
        c_id = st.text_input("Enter customer id", max_chars=50)
        p_id = st.text_input("Enter product id", max_chars=50)
        comment= st.text_input("Enter updated comment", max_chars=50)
        rate_options = [0, 1, 2, 3, 4, 5]
        rating = st.select_slider("Please provide product rating (0-5)", options=rate_options, value=1)


        if st.button("Update your Review"):
            updateReview(r_no,c_id,p_id,comment,rating)
            st.success("Review submitted !!")
        else:
            st.error("Please put all information")

    elif choice == "Delete Review":

        r_no = st.text_input("Enter review number")

        if st.button("Delete your Review"):
            deleteReview(r_no)
            st.success("Review Deleted !!")
        else:
            st.error("Please put all information")

    elif choice == "Buy Products":
        st.subheader("Our Products")

        image = Image.open(r"C:\Users\Saniya\PycharmProjects\FrontEnd\Purple elegant necklace.jpg")
        st.image(image, caption='Purple elegant necklace',width=300)
        avgr(701)
        price(701)
        if st.button("Buy Purple Necklace"):
            st.write("Reviews of this product:")
            display(701)

        image1 = Image.open(r"C:\Users\Saniya\PycharmProjects\FrontEnd\All diamonds full set.jpg")
        st.image(image1, caption='All diamonds full set',width=300)
        avgr(702)
        price(702)
        if st.button("Buy set"):
            st.write("Reviews of this product:")
            display(702)

        image2 = Image.open(r"C:\Users\Saniya\PycharmProjects\FrontEnd\Moti -perl necklace.jpg")
        st.image(image2, caption='Pearl necklace',width=300)
        avgr(703)
        price(702)
        if st.button("Buy Pearl Necklace"):
            st.write("Reviews of this product:")
            display(703)

        image3 = Image.open(r"C:\Users\Saniya\PycharmProjects\FrontEnd\necklace+Pendant.jpg")
        st.image(image3, caption='Pendant necklace',width=300)
        avgr(704)
        price(704)
        if st.button("Buy Pendant necklace"):
            st.write("Reviews of this product:")
            display(704)

        image4 = Image.open(r"C:\Users\Saniya\PycharmProjects\FrontEnd\Blue Saphire.jpg")
        st.image(image4, caption='Sapphire ring',width=300)
        avgr(710)
        price(710)
        if st.button("Buy Sapphire ring"):
            st.write("Reviews of this product:")
            display(710)

        image5 = Image.open(r"C:\Users\Saniya\PycharmProjects\FrontEnd\purple ring.jpg")
        st.image(image5, caption='Violet Ring',width=300)
        avgr(708)
        price(708)
        if st.button("Buy Violet Ring"):
            st.write("Reviews of this product:")
            display(708)

        image6 = Image.open(r"C:\Users\Saniya\PycharmProjects\FrontEnd\Siple elegant diamond ring formal.jpg")
        st.image(image6, caption='Simple Diamond ring',width=300)
        avgr(709)
        price(709)
        if st.button("Buy Simple diamond ring"):
            st.write("Reviews of this product:")
            display(709)

        image7 = Image.open(r"C:\Users\Saniya\PycharmProjects\FrontEnd\Simple gold rings.jpg")
        st.image(image7, caption='Gold earrings',width=300)
        avgr(706)
        price(706)
        if st.button("Buy Gold rings"):
            st.write("Reviews of this product:")
            display(706)

        image8 = Image.open(r"C:\Users\Saniya\PycharmProjects\FrontEnd\Emrald earring studs.jpg")
        st.image(image8, caption='Emerald studs',width=300)
        avgr(705)
        price(705)
        if st.button("Buy Emerald studs"):
            st.write("Reviews of this product:")
            display(705)

        image9 = Image.open(r"C:\Users\Saniya\PycharmProjects\FrontEnd\Royal Dangling Diamond Earrings.jpg")
        st.image(image9, caption='Royal Dangling Diamond Earrings',width=300)
        avgr(707)
        price(707)
        if st.button("Buy Diamond earrings"):
            st.write("Reviews of this product:")
            display(707)
        image = Image.open(r"C:\Users\Saniya\PycharmProjects\FrontEnd\conditions.png")
        st.image(image, caption='Our Promise!', width=300)

#calling main
if __name__ == "__main__":
    main()