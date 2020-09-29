# Lorem ipsum
Just another new header

# Text Alignment Pipeline

## Objective

Align two raw texts in different languages and extract as much parallel sentences as possible.
In this particular case there are Chinese and Russian fiction texts, but the method is the language independent and you can ajust regexps to the languages you need.

## Pipeline

The method is not in the alignment of two initial texts, but in the alignment of Russian original text and machine translated from Chinese proxy one.

- Provide the base path folder and run the pipeline, all the needed folders will be created.
- The next step of the pipeline is to split original texts to sentences (remember the mentioned regexps). We will get the two files one sentence per line.

```
['На самом краю села Мироносицкого, в сарае старосты Прокофия, расположились на ночлег запоздавшие охотники.',
 'Их было только двое: ветеринарный врач Иван Иваныч и учитель гимназии Буркин.',
 'У Ивана Иваныча была довольно странная, двойная фамилия — Чимша—Гималайский, которая совсем не шла ему, и его во всей губернии звали просто по имени и отчеству; он жил около города на конском заводе и приехал теперь на охоту, чтобы подышать чистым воздухом.',
 'Учитель же гимназии Буркин каждое лето гостил у графов П. и в этой местности давно уже был своим человеком.',
 'Не спали.',
 'Иван Иваныч, высокий худощавый старик с длинными усами, сидел снаружи у входа и курил трубку; его освещала луна.',
 'Буркин лежал внутри на сене, и его не было видно в потемках.',
 'Рассказывали разные истории.',
 'Между прочим, говорили о том, что жена старосты, Мавра, женщина здоровая и неглупая, во всю свою жизнь нигде не была дальше своего родного села, никогда не видела ни города, ни железной дороги, а в последние десять лет все сидела за печью и только по ночам выходила на улицу.',
 '— Что же тут удивительного! — сказал Буркин.— Людей, одиноких по натуре, которые, как рак—отшельник или улитка, стараются уйти в свою скорлупу, на этом свете немало.']
 ```

```
['误了时辰的猎人们在米罗诺西茨科耶村边上村长普罗科菲的堆房里住下来过夜了。',
 '他们一共只有两个人兽医伊万伊万内奇和中学教师布尔金。',
 '伊万。',
 '伊万内奇姓一个相当古怪的双姓奇姆沙吉马莱斯基，这个姓跟他一点也不相称，全省的人就简单地叫他的本名和父名伊万伊万内奇。',
 '他住在城郊一个养马场上，这回出来打猎是为了透一透新鲜空气。',
 '然而中学教师布尔金每年夏天都在伯爵家里做客，对这个地区早已熟透了。',
 '他们没睡觉。',
 '伊万伊万内奇是一个又高又瘦的老人，留着挺长的唇髭，这时候坐在门口，脸朝外，吸着烟斗。',
 '月亮照在他身上。',
 '布尔金躺在房里的干草上，在黑暗里谁也看不见他。']
 ```
### Proxy file

Using your favourite translation system get the Russian translation of the Chinese text. Amazon and Microsoft Azure offer 2M symbols per month on the free-tier plan. Put the proxy file into the proxy folder, it's name should be equal the original Russian file name.

```
Поздно охотники провели ночь в свайной комнате Прокофи, староста деревни на окраине села Мироносицкое.
Всего у них было всего два ветеринара, Иван Иванех и учитель средней школы Булкин.
Иван.
Фамилия Иванеха была довольно странным двойным именем, Чим Сагималески, которое его совсем не совпадало, и жители провинции просто называли его своим именем и фамилией отца, Иваном Иванехом.
Он жил на конной ферме на окраине города, и на этот раз он вышел на охоту, чтобы получить глоток свежего воздуха.
Но Булкин, учитель средней школы, является гостем в доме графа каждое лето, и он уже хорошо знает этот район.
Они не спали.
Иван Иванех был высоким и худым стариком с длинной губой, сидящим у двери, лицом наружу, курящим трубку.
Луна сияла на нем.
Буркин лежал на сене в комнате, и никто не мог видеть его в темноте.
```

### Sentence to vec

Then we will put the sentences to the vector space using the **Huggingface** and the pretrained **rubert-base-cased-sentence** model by DeepPavlov.

```
tokenizer = AutoTokenizer.from_pretrained("DeepPavlov/rubert-base-cased-sentence")
model = AutoModelWithLMHead.from_pretrained("DeepPavlov/rubert-base-cased-sentence")
```

### Similarity matrix

Now we can calculate the similarity matrix between all the given embeddings.

### Visualization

The amount of lines in the original texts can differ significantly and it's OK, we just need add the angle coefficient when we will search through the matrix. We'll also introduce the window parameter to not to link too distant sentences.

![Matrix](https://lingtra.in/images/other/matrix.png)

### Retrieve the pairs

After we found the pairs with some threshold we can retrieve the original Chinese sentences using the proxy file.

```
Учитель же гимназии Буркин каждое лето гостил у графов П. и в этой местности давно уже был своим человеком.

然而中学教师布尔金每年夏天都在伯爵家里做客，对这个地区早已熟透了。

Не спали.

他们没睡觉。

Буркин лежал внутри на сене, и его не было видно в потемках.

布尔金躺在房里的干草上，在黑暗里谁也看不见他。

Быть может, тут явление атавизма, возвращение к тому времени, когда предок человека не был еще общественным животным и жил одиноко в своей берлоге, а может быть, это просто одна из разновидностей человеческого характера,— кто знает?

也许这是隔代遗传的现象，重又退回从前人类祖先还不是群居的动物而是孤零零地住在各自洞穴里的时代的现象，不过，也许这只不过是人类性格的一种类型吧，谁知道呢？

Да вот, недалеко искать, месяца два назад умер у нас в городе некий Беликов, учитель греческого языка, мой товарищ.

是啊，不必往远里去找，就拿一个姓别里科夫的人来说好了，他是我的同事，希腊语教师，大约两个月前在我们城里去世了。

Он был замечателен тем, что всегда, даже в очень хорошую погоду, выходил в калошах и с зонтиком и непременно в теплом пальто на вате.

他所以出名，是因为他即使在顶晴朗的天气出门上街，也穿上套鞋，带着雨伞，而且一定穿着暖和的棉大衣。

И зонтик у него был в чехле и часы в чехле из серой замши, и когда вынимал перочинный нож, чтобы очинить карандаш, то и нож у него был в чехольчике; и лицо, казалось, тоже было в чехле, так как он все время прятал его в поднятый воротник.

他的雨伞总是装在套子里，怀表也总是装在一个灰色的麂皮套子里，遇到他拿出小折刀来削铅笔，就连那小折刀也是装在一个小小的套子里的。

Одним словом, у этого человека наблюдалось постоянное и непреодолимое стремление окружить себя оболочкой, создать себе, так сказать, футляр, который уединил бы его, защитил бы от внешних влияний.

总之，在这人身上可以看出一种经常的难忍难熬的心意，总想用一层壳把自己包起来，仿佛要为自己制造一个所谓的套子，好隔绝人世，不受外界影响。

И мысль свою Беликов также старался запрятать в футляр.

别里科夫把他的思想也极力藏在套子里。

В разрешении же и позволении скрывался для него всегда элемент сомнительный, что—то недосказанное и смутное.

他觉着在官方批准或者允许的事里面，老是包含着使人起疑的成分，包含着隐隐约约还没说透的成分。

Если кто из товарищей опаздывал на молебен, или доходили слухи о какой—нибудь проказе гимназистов, пли видели классную даму поздно вечером с офицером, то он очень волновался и все говорил, как бы чего не вышло.

要是他的一个同事参加祈祷式去迟了，或者要是他听到流言，说是中学生顽皮闹事，再不然要是有人看见一个女校的女学监傍晚陪着军官玩得很迟，他总是心慌意乱，一个劲儿地说千万别闹出什么乱子来啊。

...
```

### Optimizations & Features

#### Large files

- In order to process large files you can split them to batches and process one by one using batch_size parameter.

#### N-gramed sentences

- Translation into different language sometimes requires to split original sentence into several ones or merge sentences into one big sentence. To catch this case you can use **n_gram** parameter and "n-gram" your text into something like this (n_gram=2):

```
Дело ясное: зима, печка часто дымит, и комната полна газа.
Дело ясное: зима, печка часто дымит, и комната полна газа. Внутри окна был прибит ряд железных решеток, что было некрасиво. 
Внутри окна был прибит ряд железных решеток, что было некрасиво.
Внутри окна был прибит ряд железных решеток, что было некрасиво. Пол был бледного цвета и покрыт деревянными шипами.
```

This will help to align merged sentences from the second text. You can also adjust n-gramming with the **n_gram_sent_max_words** parameter which will combine new lines only if both sentences are long enough.
