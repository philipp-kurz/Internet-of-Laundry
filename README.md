# Internet_of_Laundry
IoL is a smart plug for communal laundry machines. It detects current flow and updates a website with machine status. Created as a final project for the class ME100 - "Electronics for the Internet of Things" at UC Berkeley during the Fall 2019 semester.

As microcontroller we used an **ESP32** programmed with **MicroPython**. The backend was built using the **LAMP stack** using an **AWS EC2** container. The backend APIs were built with **Python** and AWS's **boto3** library. Communication with the backend was done through **MQTT**. The basic **CSS** of the ffrontend came from a website template. The actual frontend was coded in vanilla **HTML**, **CSS** and **JavaScript**. The communication between frontend and backend happend through **PHP** scripts that were called through **AJAX** directly from the frontend. 

[Project details as PDF](https://github.com/philipp-kurz/CS170_NP_Comp_Approx/files/4707497/IOL_Details.pdf)

---

Product view of final version of project

![Front_small](https://user-images.githubusercontent.com/54779918/83350027-5bfd1f00-a339-11ea-8587-1e2c7b9a6f94.jpg)

---

Hardware components and project interior

![Hardware_smaller](https://user-images.githubusercontent.com/54779918/83349996-29532680-a339-11ea-843f-45ecf0f98d4e.png)

---

GIF of final website

![website](https://user-images.githubusercontent.com/54779918/83349896-6834ac80-a338-11ea-800f-305c7be9466d.gif)

Website can be found in website folder (most of code directly in index.html and IOL.js, as well as PHP scripts that were called using AJAX)
