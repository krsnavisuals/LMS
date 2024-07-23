import sqlite3
import random
from datetime import datetime

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO users (username, password) VALUES (?, ?)",
            ('Admin', 'Admin@123')
            )
dummy_users = ["StarGazer89", "TechWizard", "PeacefulWalker", "QuantumLeap2023", "NatureLover"]

for user in dummy_users:
    cur.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                (user, '1234')
                )

sections = {
    "Fiction":"Journey through invented worlds and explore the human experience.",
    "Novel": "Embark on an immersive exploration of complex narratives and rich characters.",
    "Mystery": "Unravel the enigma, follow the clues, and uncover the truth."
}

sections_list = ["Fiction", "Novel", "Mystery"]

now = datetime.now()
now_string = now.strftime("%m/%d/%Y")
for section in sections:
    cur.execute(f"INSERT INTO section (name, description, date) VALUES ('{section}', '{sections[section]}', '{now_string}');")

books = [
    {
        "name": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "description": "A novel set in the American South during the 1930s, addressing the issues of racial injustice and moral growth.",
        "price": 10.99,
        "content": "It was a hot summer day in the small town of Maycomb. Scout and her brother Jem were playing in the yard, their laughter echoing through the quiet streets. Little did they know, this day would mark the beginning of a journey that would change their lives forever. The sun beat down relentlessly, casting long shadows across the porch where Atticus Finch sat, lost in thought. He watched his children with a mixture of pride and concern, knowing the challenges they would face in the years to come. Meanwhile, Boo Radley peered out from behind the curtains of his mysterious house, his presence felt but rarely seen. As the day wore on, tensions simmered beneath the surface of the sleepy town, hinting at the deeper conflicts yet to come. And so, on this seemingly ordinary day, the stage was set for a story of courage, compassion, and the enduring power of empathy."
    },
    {
        "name": "1984",
        "author": "George Orwell",
        "description": "A dystopian novel depicting a totalitarian regime and its effects on society.",
        "price": 12.99,
        "content": "Winston Smith sat at his desk, the harsh glow of the telescreen illuminating the cramped room. He nervously glanced around, ensuring no Thought Police were watching as he began to jot down his forbidden thoughts in his secret diary. The clock struck thirteen, a reminder of the oppressive regime ruling over Oceania. Outside, the city was shrouded in a perpetual fog of fear and surveillance, its inhabitants living in a state of perpetual paranoia. Yet amidst the chaos, Winston dared to dream of rebellion, of a world where freedom still existed. With each stroke of his pen, he defied the Party and its relentless campaign of thought control. But as he looked out over the desolate landscape of Airstrip One, he couldn't shake the feeling that Big Brother was always watching, waiting to crush any flicker of dissent. And so, in this dystopian world where truth was relative and reality was a mere illusion, Winston knew that the fight for freedom would be long and treacherous."
    },
    {
        "name": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "description": "A tale of wealth, love, and the American Dream set in the Roaring Twenties.",
        "price": 11.99,
        "content": "In the glittering world of West Egg, Jay Gatsby's mansion stood as a beacon of wealth and excess. Nick Carraway, the narrator, looked out across the bay, contemplating the enigmatic figure of Gatsby and the mysteries that surrounded him. As the sun set over the horizon, whispers of parties and rumors of love filled the air. From his modest cottage next door, Nick observed the extravagant display of wealth with a mixture of awe and disdain. He longed to unravel the secrets of Gatsby's past, to understand what drove this enigmatic figure to such extravagant heights. But as he stepped into the whirlwind of glamour and deceit, Nick soon realized that the world of the rich and powerful was not as glamorous as it seemed. Beneath the façade of opulence lay a dark underbelly of greed and corruption, where love was a commodity to be bought and sold. And so, as Nick embarked on his journey of self-discovery, he learned that the pursuit of the American Dream came at a price too steep for some to pay."
    },
    {
        "name": "Pride and Prejudice",
        "author": "Jane Austen",
        "description": "A classic romance novel revolving around the themes of marriage, manners, and social status.",
        "price": 9.99,
        "content": "It is a truth universally acknowledged, that a single man in possession of a good fortune, must be in want of a wife. So begins Jane Austen's timeless tale of love and society in Regency England. Mrs. Bennet, eager to marry off her five daughters, hatches a plan to ensnare the wealthy Mr. Bingley at the next ball. Meanwhile, Elizabeth Bennet, the spirited second eldest, scoffs at her mother's matchmaking schemes, determined to marry for love rather than convenience. As the Bennet sisters navigate the treacherous waters of high society, they encounter a cast of colorful characters, from the aloof Mr. Darcy to the conniving Mr. Wickham. Amidst the gossip and intrigue of the ballroom, Elizabeth finds herself drawn to Mr. Darcy, despite her initial disdain for his haughty demeanor. But as their feelings deepen, they must confront the prejudices and misconceptions that threaten to tear them apart. With wit and charm, Austen explores the complexities of love and marriage, reminding us that true happiness can only be found when we cast aside our pride and embrace the possibility of a deeper connection."
    },
    {
        "name": "Harry Potter and the Philosopher's Stone",
        "author": "J.K. Rowling",
        "description": "The first book in the Harry Potter series, following the journey of a young wizard, Harry Potter, and his friends at Hogwarts School of Witchcraft and Wizardry.",
        "price": 14.99,
        "content": "On a seemingly ordinary day in Privet Drive, a baby with a lightning-shaped scar was delivered to the Dursleys. Unbeknownst to them, this child, Harry Potter, was destined for greatness. As Professor McGonagall watched over the sleeping infant, she knew that the wizarding world would never be the same again. Across the country, witches and wizards celebrated the downfall of the dark wizard, Voldemort, and the triumph of good over evil. But as Harry grew older, he remained unaware of his true heritage, living a life of neglect and abuse under the roof of his cruel aunt and uncle. Little did he know, he was already famous in the wizarding world, his name whispered in awe by those who remembered the night Voldemort fell. And so, as Harry embarked on his journey to Hogwarts School of Witchcraft and Wizardry, he discovered a world of magic and adventure beyond his wildest dreams. But lurking in the shadows was a darkness that threatened to consume everything he held dear, forcing him to confront his destiny as the Boy Who Lived."
    },
    {
        "name": "The Catcher in the Rye",
        "author": "J.D. Salinger",
        "description": "A coming-of-age novel following the adventures of Holden Caulfield, a teenager navigating the complexities of adulthood.",
        "price": 10.49,
        "content": "Narrated by the disillusioned teenager Holden Caulfield, The Catcher in the Rye explores themes of alienation, identity, and the transition to adulthood. After being expelled from prep school, Holden embarks on a journey through New York City, encountering various characters and grappling with feelings of isolation and confusion. Salinger's novel is a seminal work of American literature, capturing the angst and uncertainty of adolescence."
    },
    {
        "name": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "description": "A novel set in the American South during the 1930s, addressing the issues of racial injustice and moral growth.",
        "price": 10.99,
        "content": "Sample content of To Kill a Mockingbird."
    },
    {
        "name": "Moby-Dick",
        "author": "Herman Melville",
        "description": "An epic tale of obsession and revenge, centered around Captain Ahab's quest for the white whale.",
        "price": 13.99,
        "content": "Moby-Dick is an epic tale of obsession, revenge, and the struggle between man and nature. Narrated by Ishmael, the novel follows Captain Ahab's relentless quest for vengeance against the great white whale, Moby Dick, who had previously maimed him. Set aboard the whaling ship Pequod, the story explores themes of fate, morality, and the complexity of the human spirit, while delving into the intricacies of 19th-century whaling culture."
    },
    {
        "name": "The Lord of the Rings",
        "author": "J.R.R. Tolkien",
        "description": "A fantasy epic set in the fictional world of Middle-earth, following the quest to destroy the One Ring.",
        "price": 16.99,
        "content": "The Lord of the Rings is a high fantasy epic set in the fictional world of Middle-earth. The story follows Frodo Baggins, a hobbit tasked with destroying the One Ring, a powerful artifact forged by the Dark Lord Sauron. Accompanied by a fellowship of diverse companions, including elves, dwarves, and men, Frodo embarks on a perilous journey to Mount Doom, where the Ring can be destroyed. Tolkien's masterpiece explores themes of heroism, friendship, and the eternal struggle between good and evil."
    },
    {
        "name": "Jane Eyre",
        "author": "Charlotte Brontë",
        "description": "A bildungsroman novel following the life of Jane Eyre, from her abusive childhood to her independence as a governess.",
        "price": 11.49,
        "content": "Jane Eyre is a classic Victorian novel that tells the story of its eponymous protagonist, an orphaned governess who overcomes adversity to find love and independence. Raised in harsh conditions by her cruel aunt and cousins, Jane eventually secures a position at Thornfield Hall, where she falls in love with the brooding Mr. Rochester. However, dark secrets threaten their happiness, forcing Jane to confront her own values and desires. Brontë's novel is celebrated for its exploration of social class, gender roles, and the pursuit of personal integrity in the face of societal expectations."
    }
]

for book in books:
    cur.execute("INSERT INTO books (name, author, description, price, content, section, date_issued, return_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (book['name'], book['author'], book['description'], book['price'], book['content'], random.choice(sections_list), "-", "-")
        )

reviews = [
    "Loved this book! It made me laugh and cry. A real page-turner.",
    "It started strong but got a bit slow in the middle. Still good though.",
    "The characters felt like real people. I miss them already.",
    "The places in the book felt so real, like I could visit them.",
    "Wish the ending was different, but overall, a great read.",
    "Some parts were confusing, but maybe I just need to read it again.",
    "Perfect for anyone who loves adventure. I couldn't put it down!",
    "Not my usual type of book, but I'm glad I gave it a chance.",
    "The main character was so brave. Made me want to be braver too.",
    "Needed more action! But if you like quiet stories, you might like it.",
    "I learned a lot from this book. It makes you think.",
    "Some words were hard to understand, but the story was worth it.",
    "I loved the jokes and fun moments. It's not all serious.",
    "Felt like the story ended too soon. I wanted more!",
    "The friendship in the story is goals. Made me appreciate my friends more.",
    "There's a twist I didn't see coming. Made my jaw drop.",
    "Wished for more pictures to see what things looked like.",
    "It's a cozy book. Good for reading on a rainy day.",
    "I liked the book, but my friend didn't. Guess it's not for everyone.",
    "Easy to read and hard to forget. I keep thinking about the story.",
]

for review in reviews:
    cur.execute("INSERT INTO book_review (book_id, username, description) VALUES (?, ?, ?)",
            (random.randint(1,10), random.choice(dummy_users), review)
        )

connection.commit()
connection.close()