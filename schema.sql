-- =============================================
-- The View - Supabase Database Schema
-- Run this entire file in the Supabase SQL Editor
-- =============================================

-- Enable UUID generation
create extension if not exists "pgcrypto";

-- =============================================
-- published (approved news articles)
-- =============================================
create table if not exists published (
  id              uuid primary key default gen_random_uuid(),
  title           text,
  description     text,
  url             text,
  "urlToImage"    text,
  publisher       text,
  category        text,
  "publishedAt"   text,
  "createdAt"     text,
  hashtags        jsonb default '[]'::jsonb,
  keyplayers      jsonb default '[]'::jsonb,
  sentiment       text,
  sentiment_compound float,
  desc_line       text,
  source          text
);

create index if not exists idx_published_category    on published (category);
create index if not exists idx_published_created_at  on published ("createdAt" desc);
create index if not exists idx_published_title       on published (title);
create index if not exists idx_published_desc_line   on published (desc_line);
create index if not exists idx_published_description on published (description);

-- =============================================
-- unpublished (pending / draft news)
-- =============================================
create table if not exists unpublished (
  id              uuid primary key default gen_random_uuid(),
  title           text,
  description     text,
  url             text,
  "urlToImage"    text,
  publisher       text,
  category        text,
  "publishedAt"   text,
  "createdAt"     text,
  hashtags        jsonb default '[]'::jsonb,
  keyplayers      jsonb default '[]'::jsonb,
  sentiment       text,
  sentiment_compound float,
  desc_line       text,
  source          text
);

create index if not exists idx_unpublished_category   on unpublished (category);
create index if not exists idx_unpublished_created_at on unpublished ("createdAt" desc);

-- =============================================
-- sponsored (sponsored / ad articles)
-- =============================================
create table if not exists sponsored (
  id              uuid primary key default gen_random_uuid(),
  title           text,
  description     text,
  url             text,
  "urlToImage"    text,
  publisher       text,
  category        text,
  "publishedAt"   text,
  "createdAt"     text,
  hashtags        jsonb default '[]'::jsonb,
  keyplayers      jsonb default '[]'::jsonb,
  sentiment       text,
  sentiment_compound float,
  desc_line       text
);

create index if not exists idx_sponsored_category   on sponsored (category);
create index if not exists idx_sponsored_created_at on sponsored ("createdAt" desc);

-- =============================================
-- video
-- =============================================
create table if not exists video (
  id           uuid primary key default gen_random_uuid(),
  title        text,
  description  text,
  url          text,
  "contentUrl" text,
  "thumbnailUrl" text,
  publisher    text,
  "publishedAt" text,
  "createdAt"  text
);

create index if not exists idx_video_created_at on video ("createdAt" desc);
create index if not exists idx_video_title      on video (title);

-- =============================================
-- hashtags  (tag_name is the unique key)
-- =============================================
create table if not exists hashtags (
  id       uuid primary key default gen_random_uuid(),
  tag_name text unique not null,
  count    integer default 1,
  ids      jsonb default '[]'::jsonb
);

create index if not exists idx_hashtags_tag_name on hashtags (tag_name);
create index if not exists idx_hashtags_count    on hashtags (count desc);

-- =============================================
-- keyplayer  (name is the unique key)
-- =============================================
create table if not exists keyplayer (
  id           uuid primary key default gen_random_uuid(),
  name         text unique not null,
  count        integer default 1,
  ids          jsonb default '[]'::jsonb,
  "urlToImage" text
);

create index if not exists idx_keyplayer_name  on keyplayer (name);
create index if not exists idx_keyplayer_count on keyplayer (count desc);

-- =============================================
-- deviceinfo  (push-notification device tokens)
-- =============================================
create table if not exists deviceinfo (
  id                   uuid primary key default gen_random_uuid(),
  token                text,
  date                 text,
  category_preference  jsonb default '["trending"]'::jsonb,
  key_preference       jsonb default '[]'::jsonb,
  hashtag_preference   jsonb default '[]'::jsonb
);

create index if not exists idx_deviceinfo_token on deviceinfo (token);

-- =============================================
-- Row-Level Security
-- Allow the service-role key full access;
-- anon key can read published/video/hashtags/keyplayer
-- =============================================

alter table published    enable row level security;
alter table unpublished  enable row level security;
alter table sponsored    enable row level security;
alter table video        enable row level security;
alter table hashtags     enable row level security;
alter table keyplayer    enable row level security;
alter table deviceinfo   enable row level security;

-- Public read on content tables
create policy "public read published"  on published   for select using (true);
create policy "public read video"      on video       for select using (true);
create policy "public read hashtags"   on hashtags    for select using (true);
create policy "public read keyplayer"  on keyplayer   for select using (true);

-- Service role gets full access (all tables)
create policy "service full published"   on published   for all using (true) with check (true);
create policy "service full unpublished" on unpublished for all using (true) with check (true);
create policy "service full sponsored"   on sponsored   for all using (true) with check (true);
create policy "service full video"       on video       for all using (true) with check (true);
create policy "service full hashtags"    on hashtags    for all using (true) with check (true);
create policy "service full keyplayer"   on keyplayer   for all using (true) with check (true);
create policy "service full deviceinfo"  on deviceinfo  for all using (true) with check (true);
