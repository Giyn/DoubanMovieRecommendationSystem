# DoubanMovieRecommendationSystem

[![](https://img.shields.io/badge/release-beta-blue.svg)](https://github.com/Giyn/DoubanMovieRecommendationSystem/releases/tag/1.0.0) [![](https://img.shields.io/badge/version-1.0.0-red.svg)](https://github.com/Giyn/DoubanMovieRecommendationSystem/releases/tag/1.0.0) [![](https://img.shields.io/badge/build-passing-green.svg)](https://github.com/Giyn/DoubanMovieRecommendationSystem/releases/tag/1.0.0)



## :blue_book: Introduction

豆瓣电影推荐系统——通过爬取电影数据和用户数据，再利用所爬取的数据设计并实现相关推荐算法对用户进行电影推荐。然后设计出图形用户界面（GUI）进行交互，封装成电影推荐软件，针对数据集中的用户推荐相关电影。

**主要分为三大模块：**

:one: 爬虫模块：request 库、json 库、MySQL 

:two: 推荐系统模块：基于物品的协同过滤算法（ItemCF 算法）

:three: GUI 模块：PyQt5



## :point_right: Instruction

运行 GUI 文件夹中的 `main.py` 文件即可。



## :smile: Information

开发者：许继元

联系邮箱：giyn.jy@gmail.com

项目开发时间：2020-05-01至 2020-05-13

版本号：1.0.0



## :mag_right: ​Algorithm

ItemCF 算法不利用物品的内容属性计算物品之间的相似度，而是通过分析用户的行为记录计算物品之间的相似度。ItemCF 算法认为，物品 A 和物品 B 具有很大的相似度是因为喜欢物品 A 的用户大都也喜欢物品 B。

 

#### **ItemCF 算法步骤：**

\-    计算物品之间的相似度。

\-    根据物品的相似度和用户的历史行为给用户生成推荐列表。



简单来说，ItemCF 算法给用户推荐那些和他们之前喜欢的物品相似的物品。



##### 举个例子：

| **用户**/**物品** | **物品 A** | **物品 B** |     **物品 C**      |
| :---------------: | :--------: | :--------: | :-----------------: |
|      用户 A       |     √      |            |          √          |
|      用户 B       |     √      |     √      |          √          |
|      用户 C       |     √      |            | 与物品 A 相似，推荐 |



## :bulb: ​Features

#### 1.登录注册界面

登录注册界面是经典的用户图形界面，在 QQ 等平台都有类似的界面，在 `users_info.csv` 数据集中随便选取一名用户的用户名和密码输入，即可成功登录。

![登录注册界面.png](https://github.com/Giyn/DoubanMovieRecommendationSystem/blob/master/Screenshot/%E7%99%BB%E5%BD%95%E6%B3%A8%E5%86%8C%E7%95%8C%E9%9D%A2.png?raw=true)



#### 2.用户主界面

登录成功后进入用户主界面，界面的左边是个性化推荐板块，右边是热门电影板块。

![用户主界面.png](https://github.com/Giyn/DoubanMovieRecommendationSystem/blob/master/Screenshot/%E7%94%A8%E6%88%B7%E4%B8%BB%E7%95%8C%E9%9D%A2.png?raw=true)



#### 3.电影搜索界面

进入用户主界面之后，通过点击“电影搜索”按钮，可以进入电影搜索界面，该搜索界面支持模糊搜索。例如输入复仇者联盟，即可看到复仇者联盟这一系列的电影。

<img src="https://github.com/Giyn/DoubanMovieRecommendationSystem/blob/master/Screenshot/%E7%94%B5%E5%BD%B1%E6%90%9C%E7%B4%A2%E7%95%8C%E9%9D%A2.png?raw=true" alt="电影搜索界面.png" style="zoom: 50%;" />



#### 4.电影详情界面

在用户主界面中，通过点击“电影详细页面”按钮，可以进入电影详细信息的搜索界面，通过输入完整的电影名称（例如：千与千寻），我们可以了解电影的详细信息，如导演、编剧、主演、电影简介等信息都可以看到。

![电影详情界面.png](https://github.com/Giyn/DoubanMovieRecommendationSystem/blob/master/Screenshot/%E7%94%B5%E5%BD%B1%E8%AF%A6%E6%83%85%E7%95%8C%E9%9D%A2.png?raw=true)



#### 5.用户个人界面

进入主界面后，有一个“个人主页”按钮，点击之后，简单的个人信息显示如下。

![用户个人界面.png](https://github.com/Giyn/DoubanMovieRecommendationSystem/blob/master/Screenshot/%E7%94%A8%E6%88%B7%E4%B8%AA%E4%BA%BA%E7%95%8C%E9%9D%A2.png?raw=true)



## :high_brightness: Optimization

#### 用户的冷启动问题

用户新注册时，会弹出一个窗口，询问用户喜欢的电影类型，此处输入“喜剧”进行测试，可以看到，根据用户喜欢的电影类型给用户进行了个性化推荐。

<img src="https://github.com/Giyn/DoubanMovieRecommendationSystem/blob/master/Screenshot/%E6%B3%A8%E5%86%8C%E7%95%8C%E9%9D%A2.png?raw=true" alt="注册界面.png" style="zoom: 67%;" />



<img src="https://github.com/Giyn/DoubanMovieRecommendationSystem/blob/master/Screenshot/%E6%88%90%E5%8A%9F%E6%B3%A8%E5%86%8C.png?raw=true" alt="成功注册.png" style="zoom: 67%;" />



<img src="https://github.com/Giyn/DoubanMovieRecommendationSystem/blob/master/Screenshot/%E7%94%A8%E6%88%B7%E7%9A%84%E5%86%B7%E5%90%AF%E5%8A%A8%E9%97%AE%E9%A2%98.png?raw=true" alt="用户的冷启动问题.png" style="zoom: 50%;" />



<img src="https://github.com/Giyn/DoubanMovieRecommendationSystem/blob/master/Screenshot/%E7%94%A8%E6%88%B7%E7%9A%84%E5%86%B7%E5%90%AF%E5%8A%A8%E9%97%AE%E9%A2%98%EF%BC%88%E6%B5%8B%E8%AF%95%EF%BC%89.png?raw=true" alt="用户的冷启动问题（测试）.png" style="zoom: 67%;" />



##  :heavy_exclamation_mark: License

本软件仅供学习与参考，请勿用于商业用途

Copyright 许继元

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at 

```
  http://www.apache.org/licenses/LICENSE-2.0
```

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License. 

