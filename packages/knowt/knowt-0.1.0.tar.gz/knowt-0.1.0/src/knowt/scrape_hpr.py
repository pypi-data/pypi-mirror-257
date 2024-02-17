import bs4
import pandas as pd
import requests
from tqdm import tqdm


def scrape_index(url='https://hackerpublicradio.org/eps/index.html'):
    resp = requests.get(url)
    bs = bs4.BeautifulSoup(resp.text)
    episodes = [
        [ep['href'], ep.text, ep.next_sibling.next_sibling['href'], ep.next_sibling.next_sibling.text]
        for ep in bs.find_all('a') if ep.get('href', '').startswith('./eps/hpr')
    ]
    df = pd.DataFrame(episodes, columns='url full_title host_url host_name'.split())
    df = df.sort_values('url')
    df = df.reset_index(drop=True)
    df['seq_num'] = df.index.values + 1
    df['title'] = df['full_title'].str.split('::').str[-1]
    return df['seq_num title url host_name host_url full_title'.split()]


def scrape_episode(url='./eps/hpr0030/'):
    if url.lstrip('.').lstrip('/').startswith('eps/hpr'):
        url = '/'.join(['https://hackerpublicradio.org', url.lstrip('.').lstrip('/')])
    resp = requests.get(url)
    s = bs4.BeautifulSoup(resp.text)
    title, comments = s.find_all('h1')[1:3]
    subtitle, series = s.find_all('h3')[1:3]
    show_notes = list(series.next_siblings)[-1].next.next_sibling
    links = list(series.parent.find_all('a'))
    tags = [
        a.text for a in links
        if a.get('href', '').lstrip('.').lstrip('/').startswith('tags.html#')
    ]
    audio = [a.get('href', '') for a in links if (a.text.lower().strip() in 'ogg spx mp3')]
    row = dict(
        full_title_4digit=title.text,
        subtitle=subtitle.text,
        series=series.text,
        audio=audio,
        show_notes=show_notes.text,
        tags=tags)
    series.parent.find_all('a')
    return row


if __name__ == '__main__':
    df = scrape_index()
    episodes = []
    for url in tqdm(df['url']):
        print(url)
        episodes += [scrape_episode(url)]
    if len(df) == len(episodes):
        df = pd.concat([df, pd.DataFrame(episodes)], axis=1)
    df.to_csv('data/hpr_podcasts.csv', index=None)
