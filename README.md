# Commerce

An online auction platform built with Django as part of Harvard's CS50W course. Users can create auction listings, place bids, maintain a watchlist, browse by category, comment on listings, and close auctions.

---

## Features

- User registration and authentication
- Create, edit, and manage auction listings
- Place bids with automatic bid validation
- Personal watchlist
- Browse listings by category
- Comment on auction listings
- Close auctions and determine the winner
- Responsive and clean user interface

---

## Tech Stack

- Python
- Django
- HTML
- CSS
- SQLite

---

## Project Structure

```
commerce/
│
├── auctions/
├── commerce/
├── screenshots/
├── README.md
├── requirements.txt
├── manage.py
└── .gitignore
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/kunal9939/commerce.git
```

Move into the project directory

```bash
cd commerce
```

Create a virtual environment

```bash
python -m venv venv
```

Activate it

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Apply migrations

```bash
python manage.py migrate
```

Run the development server

```bash
python manage.py runserver
```

Visit

```
http://127.0.0.1:8000/
```

---

## Screenshots

### Home Page

![Home](screenshots/home.png)

---

### Auction Listing

![Listing](screenshots/listing.png)

---

### Watchlist

![Watchlist](screenshots/watchlist.png)

---

### Categories

![Categories](screenshots/categories.png)

---

### Create Listing

![Create Listing](screenshots/create_listing.png)

---

## Skills Demonstrated

- Django Models
- URL Routing
- Views
- Django Templates
- User Authentication
- Database Relationships
- Form Handling
- CRUD Operations
- Static File Management

---

## Future Improvements

- Search functionality
- Pagination
- User profile pages
- Image upload support
- Improved UI/UX
- Email notifications

---

## License

This project was developed for educational purposes as part of Harvard's CS50W course.