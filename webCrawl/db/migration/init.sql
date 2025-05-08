create table crawl (
    id serial primary key,
    url text NOT NULL,
    title text,
    content text,
    crawled_at timestamp with time zone default (now() at time zone 'Asia/Tokyo')
);
