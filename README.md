# Anime Popularity and Recommendation Analysis

A comprehensive data analysis project that involves scraping, cleaning, and processing anime data from multiple sources to generate insights and recommendations. This project integrates data from an Arabic website, MyAnimeList, and AniList to provide a thorough analysis of anime popularity and generate personalized recommendations.

**Note**: This project is part of a larger initiative. As such, you may find some unused data and code snippets.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Technologies Used](#technologies-used)
3. [Results and Insights](#results-and-insights)
4. [Areas for Improvement](#areas-for-improvement)
5. [Limitations](#limitations)
6. [Demo](#demo)
7. [Contact](#contact)

## Project Overview

This project involves a series of data processing and analysis steps:

1. **Data Scraping**: 
   - **Arabic Website**: Scrape anime data using Scrapy.
   - **MyAnimeList**: Scrape additional data using Playwright.
   - **AniList API**: Fetch recommendations based on MyAnimeList IDs.

2. **Data Cleaning and Processing**: 
   - Clean and prepare data from both sources.
   - Merge data using MyAnimeList IDs to enrich the dataset with recommendations.

3. **Data Analysis**:
   - Generate insights on category performance in Arabic content.
   - Create a scoring system based on average views, comments, and ratings.
   - Scale and sort data according to the calculated scores.

4. **Model Application**:
   - Use a Gemini-tuned model to provide detailed comparisons and recommendations between anime titles.

5. **Publishing**:
   - Publish the final analysis and recommendations online using the Blogger API.
### Example Input
```
{
  "anime1": "Nakitai Watashi wa Neko wo Kaburu",
  "anime2": "Kimi no Na wa."
}

```
### Example Output

**Arabic:**
```json
{
  "intro": "يُعد كل من أنمي Nakitai Watashi wa Neko wo Kaburu (أريد أن أبكي وأرتدي قناع قطة) و Kimi no Na wa. (اسمك) من الأعمال الفنية المتميزة في عالم الأنمي، حيث حظيا بشعبية كبيرة ونالا إعجاب العديد من المشاهدين. على الرغم من اختلاف قصصهما وشخصياتهما، إلا أنهما يتشاركان بعض أوجه التشابه والاختلاف التي تجعلهما مثيرين للاهتمام للمقارنة.",
  "similarties": [
    {"point": "العناصر الخيالية", "details": "يتضمن كل من الأنميين عناصر خيالية تلعب دورًا مهمًا في تطوير القصة. في Nakitai Watashi wa Neko wo Kaburu، يمكن لبطلة الرواية، Miyo Sasaki، أن تتحول إلى قطة باستخدام قناع سحري، بينما في Kimi no Na wa.، يتبادل بطلا الرواية، Taki Tachibana و Mitsuha Miyamizu، الأجساد بشكل غامض."},
    {"point": "التبادل", "details": "يلعب التبادل دورًا مركزيًا في كلتا القصتين. في Nakitai Watashi wa Neko wo Kaburu، تتبادل Miyo هويتها مع قطة تدعى Taro، بينما في Kimi no Na wa.، يتبادل Taki و Mitsuha أجسادهما."},
    {"point": "الحب غير المتبادل", "details": "تُعاني كلتا بطلتي الرواية من حب غير متبادل. في Nakitai Watashi wa Neko wo Kaburu، تحب Miyo زميلها في الفصل، Kento Hinode، لكنه لا يبادلها المشاعر، بينما في Kimi no Na wa.، تحب Mitsuha زميلها في الفصل، Taki، لكنهما لا يعرفان بعضهما البعض."},
    {"point": "الموسيقى التصويرية الجميلة", "details": "تُعد الموسيقى التصويرية لكل من الأنميين من نقاط قوتهما. تتضمن الموسيقى مزيجًا من الألحان العاطفية والإيقاعات الهادئة التي تعزز الأجواء وتكمل القصة."},
    {"point": "الشعور بالوحدة", "details": "تستكشف كلتا القصتين موضوع الشعور بالوحدة والعزلة. تكافح Miyo و Taki للعثور على مكانهما في العالم ويشعران بالوحدة على الرغم من وجود الآخرين من حولهم."},
    {"point": "الرسوم المتحركة الرائعة", "details": "يتميز كل من الأنميين برسوم متحركة عالية الجودة وتفاصيل معقدة. تعزز الرسوم المتحركة الجميلة الأجواء وتجعل المشاهدين منغمسين في القصة."},
    {"point": "الشعبية", "details": "حظي كل من الأنميين بشعبية كبيرة في اليابان وخارجها. لقد حققا نجاحًا تجاريًا ونقديًا، وحصلا على العديد من الجوائز والتقدير."}
  ],
  "diffrancies": [
    {"point": "القصة", "details": "تختلف قصص الأنميين بشكل كبير. في Nakitai Watashi wa Neko wo Kaburu، تركز القصة على Miyo وهي تحاول التعبير عن مشاعرها من خلال ارتداء قناع قطة، بينما في Kimi no Na wa.، تركز القصة على Taki و Mitsuha وهما يحاولان التواصل مع بعضهما البعض بعد تبادل أجسادهما."},
    {"point": "الشخصيات", "details": "تختلف شخصيات الأنميين أيضًا. Miyo هي فتاة خجولة ومنطوية على نفسها، بينما Taki هو فتى واثق من نفسه ومنفتح. Mitsuha هي فتاة قوية الإرادة ومستقلة، بينما Kento هو فتى لطيف ومهتم."},
    {"point": "الأسلوب", "details": "يتميز Nakitai Watashi wa Neko wo Kaburu بأسلوب أكثر واقعية وطبيعي، بينما يتميز Kimi no Na wa. بأسلوب أكثر خيالية ورائع. يستخدم Nakitai Watashi wa Neko wo Kaburu ألوانًا أكثر هدوءًا وطبيعية، بينما يستخدم Kimi no Na wa. ألوانًا أكثر حيوية وحيوية."}
  ]
}
```
**English Translation:**
```
{
  "intro": "Both Nakitai Watashi wa Neko wo Kaburu and Kimi no Na wa. are exceptional works in the anime world, enjoying great popularity and acclaim from viewers. Despite differing stories and characters, they share similarities and differences that make them interesting for comparison.",
  "similarties": [
    {"point": "Fantasy Elements", "details": "Both anime feature fantasy elements that play a crucial role in the story development. In Nakitai Watashi wa Neko wo Kaburu, the protagonist, Miyo Sasaki, can transform into a cat using a magical mask, while in Kimi no Na wa., the protagonists, Taki Tachibana and Mitsuha Miyamizu, mysteriously exchange bodies."},
    {"point": "Exchange", "details": "Exchange plays a central role in both stories. In Nakitai Watashi wa Neko wo Kaburu, Miyo exchanges her identity with a cat named Taro, while in Kimi no Na wa., Taki and Mitsuha exchange their bodies."},
    {"point": "Unrequited Love", "details": "Both protagonists suffer from unrequited love. In Nakitai Watashi wa Neko wo Kaburu, Miyo loves her classmate Kento Hinode, who does not reciprocate her feelings, while in Kimi no Na wa., Mitsuha loves her classmate Taki, but they do not know each other."},
    {"point": "Beautiful Soundtrack", "details": "The soundtrack of both anime is a strong point. It features a mix of emotional melodies and soothing rhythms that enhance the atmosphere and complement the story."},
    {"point": "Sense of Loneliness", "details": "Both stories explore the theme of loneliness and isolation. Miyo and Taki struggle to find their place in the world and feel lonely despite being surrounded by others."},
    {"point": "Stunning Animation", "details": "Both anime feature high-quality animation and intricate details. The beautiful animation enhances the atmosphere and immerses viewers in the story."},
    {"point": "Popularity", "details": "Both anime have enjoyed significant popularity in Japan and beyond. They have achieved commercial and critical success, receiving numerous awards and accolades."}
  ],
  "diffrancies": [
    {"point": "Story", "details": "The stories of the two anime differ significantly. Nakitai Watashi wa Neko wo Kaburu focuses on Miyo trying to express her feelings by wearing a cat mask, while Kimi no Na wa. focuses on Taki and Mitsuha trying to connect with each other after exchanging bodies."},
    {"point": "Characters", "details": "The characters also differ. Miyo is a shy and introverted girl, while Taki is a confident and outgoing boy. Mitsuha is a strong-willed and independent girl, while Kento is a kind and caring boy."},
    {"point": "Style", "details": "Nakitai Watashi wa Neko wo Kaburu has a more realistic and natural style, while Kimi no Na wa. features a more fantastical and vibrant style. Nakitai Watashi wa Neko wo Kaburu uses calmer and natural colors, while Kimi no Na wa. uses more vivid and lively colors."}
  ]
}
```

## Technologies Used

- **Scrapy**: For scraping data from the Arabic website.
- **Playwright**: For scraping data from MyAnimeList.
- **Blogger API**: For publishing the final results online.
- **Gemini Model**: For detailed comparisons and recommendations.
- **Google Colab**: For executing code.

## Results and Insights

- **Popularity Analysis**: Identified top anime based on views, comments, and ratings.
- **Category Analysis**: Evaluated which anime categories are more popular in Arabic content compared to global trends.
- **Recommendations**: Generated personalized recommendations based on the data.

## Areas for Improvement

- **Model Enhancement**: Add more inputs to control the tone and language.
- **Automated Pipeline**: Create an automated pipeline to streamline and automate the entire process.

## Limitations

- **Single Arabic Source**: Only one Arabic source was used for scraping, which limits the comprehensiveness of the data. Cross-validation with multiple sources is needed to ensure more accurate results.
- **Machine Learning Methods**: The recommendation system primarily relies on AniList data, which may not fully represent Arabic content. There are limitations in applying item-based or user-based recommendation methods effectively.
- **LLM Model**: The free LLM model used for analysis is slow and restricted to 1600 requests per day. A paid model with unlimited access and parallel programming capabilities would provide faster results and handle more extensive queries.

## Demo

[Link to Demo](https://topanimemaster.blogspot.com/2024/06/kimetsu-no-yaiba-movie-mugen-ressha-hen.html)

## Contact

For any questions or feedback, please reach out to Ahmed Attia Ramadan at [email](mailto:ahmedatia456123@gmail.com).
