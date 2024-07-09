drop table if exists Book;
CREATE TABLE Book (
    id VARCHAR(255) PRIMARY KEY,
    author VARCHAR(255),
    title VARCHAR(255),
    pages INT,
    short_text TEXT,
    msdn VARCHAR(255),
    image VARCHAR(255)
);
INSERT INTO Book (id, author, title, pages, short_text, msdn, image)
VALUES
    ('some_unique_id_1', 'John Doe', 'The Great Adventure', 300, 'An epic journey through uncharted lands.', 'https://example.com/book1', 'test1.png'),
    ('some_unique_id_2', 'Jane Smith', 'Mystery at Midnight', 250, 'A thrilling detective novel.', 'https://example.com/book2', 'test2.png'),
    ('some_unique_id_3', 'Alice Johnson', 'The Enigma Code', 400, 'A gripping historical thriller.', 'https://example.com/book3', 'test3.png'),
    ('some_unique_id_4', 'Robert Lee', 'Beyond the Stars', 320, 'An intergalactic adventure.', 'https://example.com/book4', 'test5.png'),
    ('some_unique_id_5', 'Emily White', 'Whispers in the Woods', 280, 'A haunting mystery set in a secluded forest.', 'https://example.com/book5', 'test6.png'),
    ('some_unique_id_6', 'David Brown', 'The Quantum Paradox', 350, 'Exploring the boundaries of reality.', 'https://example.com/book6', 'test7.png'),
    ('some_unique_id_7', 'Sophia Adams', 'Lost in Time', 290, 'A time-travel romance.', 'https://example.com/book7', 'test1.png'),
    ('some_unique_id_8', 'Michael Green', 'City of Neon Dreams', 380, 'Cyberpunk noir in a dystopian metropolis.', 'https://example.com/book8', 'test2.png'),
    ('some_unique_id_9', 'Lily Chen', 'Silent Echoes', 310, 'A poignant family saga.', 'https://example.com/book9', 'test6.png'),
    ('some_unique_id_10', 'Daniel Rodriguez', 'Sands of Destiny', 270, 'An archaeological adventure in Egypt.', 'https://example.com/book10', 'test3.png'),
    ('77669b5e-fac6-4df1-9fa9-77041a431d31','Master','Margarita',123,'asdasd','interesting read','master.jpeg'
);
