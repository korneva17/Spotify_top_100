import pandas as pd
from typing import List, Any, Dict, Optional
import json
import unittest

spotify_songs = pd.read_csv('spotify_songs_top_100.csv')


def date_format(date: str) -> str:
  '''Функция принимает даты в разных форматах и приводит к единому формату:\
   ГГГГ-ММ-ДД, отсекая время'''
  date = pd.to_datetime(date, dayfirst=True)
  string_date: str = str(date)
  splitted_date: str = string_date.split()
  return splitted_date[0]


for i in range(len(spotify_songs['Release Date'])):
  spotify_songs.loc[i, 'Release Date'] = date_format(spotify_songs.loc[i, 'Release Date'])


class TestDate(unittest.TestCase):
  def test_date_with_dots(self):
    self.assertEqual(date_format('10.May.19'), '2019-05-10')
  def test_date_wiht_dots_1(self):
    self.assertEqual(date_format('10.May.2019'), '2019-05-10')
  def test_date_without_dots(self):
    self.assertEqual(date_format('10 May 19'), '2019-05-10')
  def test_date_without_dots_1(self):
    self.assertEqual(date_format('10 May 2019'), '2019-05-10')
  def test_date_without_dots_2(self):
    self.assertEqual(date_format('1May 2019'), '2019-05-01')
  def test_date_without_dots_3(self):
    self.assertEqual(date_format('1May2019'), '2019-05-01')
  def test_date_variation(self):
    self.assertEqual(date_format('10 May.2019'), '2019-05-10')
  def test_date_variation_1(self):
    self.assertEqual(date_format('10.May 2019'), '2019-05-10')

unittest.main(argv = [''], verbosity=2, exit=False)


def songs_by_sheeran(df: Any) -> List[str]:
  '''Функция принимает Датафрейм, находит строки в столбце Artist, которые содержат слова Ed Sheeran\
  возвращает список песен, которые исполняет Ed Sheeran (в том числе с кем-то)'''
  sheeran_songs = df[df['Artist'].str.contains('Ed Sheeran')]
  sheeran_songs_list: List[str] = list(sheeran_songs.Song)
  return sheeran_songs_list


ed_sheeran_songs: List[str] = songs_by_sheeran(spotify_songs) 


def three_oldest_songs(df: Any) -> List[str]:
  '''Функция принимает Датафрейм, сортирует песни по дате выхода, возвращает\
   список из 3 самых старых песен'''
  sorted_songs = df.sort_values(by='Release Date', ascending=True)
  old_songs_first_3: List[str] = list(sorted_songs.Song.head(3))
  return old_songs_first_3


oldest_songs: List[str] = three_oldest_songs(spotify_songs)


def splitting_artists(df: Any) -> Any:
 '''Функция принимает Датафрейм и возвращает другой Датафрейм, в котором ячейки первого\
  Датафрейма, содержавшие 'and' и 'featuring', разделяются по этим словам'''
 artist_streams_df = df.loc[:, ['Streams (Billions)', 'Artist']]
 artist_streams_df[['Artist', 'Other Artist']] = artist_streams_df['Artist'].str.split(' and ', 1, expand= True)
 artist_streams_df[['Artist', 'Featuring Artist']] = artist_streams_df['Artist'].str.split(' featuring ', 1, expand= True)
 artist_streams_df[['Other Artist', 'Featuring Artist 2']] = artist_streams_df['Other Artist'].str.split(' featuring ', 1, expand= True)
 return artist_streams_df


def counting_streams_by_artist(df: Any) -> Dict[Optional[str], float]:
 '''Функция принимает Датафрейм и возвращает словарь, в котором находится\
  сумма прослушиваний для всех песен каждого исполнителя'''
 df['Streams (Billions)'] = df['Streams (Billions)'].str.replace(',','.')
 df['Streams (Billions)'] = df['Streams (Billions)'].astype(float)
 results: Dict[Optional[str], float] = {}
 rows: List[str] = ['Artist', 'Other Artist', 'Featuring Artist', 'Featuring Artist 2']
 for row in rows:
  for i in range(len(df)):
   if df.loc[i, row] not in results:
     results[df.loc[i, row]] = df.loc[i, 'Streams (Billions)']
   else:
     results[df.loc[i, row]] += df.loc[i, 'Streams (Billions)']
 return(results)


splitted_artists = splitting_artists(spotify_songs)
counted_streams: Dict[Optional[str], float] = counting_streams_by_artist(splitted_artists)
counted_streams.pop(None)

spotify_data = {
    'Ed Sheeran sings': ed_sheeran_songs,
   'Three oldest popular songs': oldest_songs, 
   'Artits and their streams (Billions)': counted_streams
}
with open('spotify_answers.json', 'w') as f:
    json.dump(spotify_data, f)


import matplotlib.pyplot as plt
spotify_songs['Release Year'] = spotify_songs['Release Date']
release_years = spotify_songs.loc[:, 'Release Year']
for i in range(len(spotify_songs['Release Year'])):
  spotify_songs.loc[i, 'Release Year'] = spotify_songs.loc[i, 'Release Year'][0:4]
sorted_songs_by_year = spotify_songs.sort_values(by='Release Year')
release_years = sorted_songs_by_year['Release Year']
plt.hist(release_years, alpha = 0.5, color = 'mediumseagreen', bins = 18)
plt.xticks(fontsize=7, rotation=30)
plt.title('Популярные песни на Spotify в зависимости от года', color = 'darkslategrey')
plt.xlabel('Год', fontsize = 8)
plt.ylabel('Количество популярных песен')
plt.savefig('Популярные песни на Spotify по годам.png')