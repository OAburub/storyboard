"""Build the TEST3 rain formation video storyboard."""
import sys, os
_p = os.popen('git rev-parse --show-toplevel 2>/dev/null').read().strip() or os.getcwd()
sys.path.insert(0, os.path.join(_p, '.claude', 'skills', 'storyboard-generator', 'scripts'))
from docx_engine import VideoBuilder

builder = VideoBuilder(
    project_code='TEST3',
    unit_number=1,
    unit_name='كيف يتكوّن المطر؟',
    project_name='فيديو تعليمي — تكوّن المطر',
    institution='مدرسة ابتدائية',
    designer='',
)
builder.set_element_name('فيديو موشن — كيف يتكوّن المطر؟')
builder.set_element_code('TEST3_U01_Video')

# === SCENE 1: Introduction (HTML+CSS screenshot) ===
builder.add_scene(
    title='مقدمة — من أين يأتي المطر؟',
    screen_description='مشهد افتتاحي ملون يعرض سماء زرقاء مع سحب بيضاء وقطرات مطر متساقطة. يظهر في الوسط سؤال كبير يثير فضول الطلاب: من أين تأتي قطرات المطر؟ مع أرضية خضراء في الأسفل وشمس مشرقة في الزاوية.',
    sound_effects='موسيقى مرحة وخفيفة مع صوت قطرات مطر هادئة',
    narration_segments=[
        {
            'narration': 'هل تساءلت يومًا... من أين يأتي المطر؟ عندما تنظر إلى السماء وترى قطرات الماء تتساقط... من أين جاءت؟',
            'on_screen_text': 'كيف يتكوّن المطر؟',
            'scene_description': 'بالتزامن مع بداية السرد، تظهر السماء الزرقاء تدريجيًا مع سحب بيضاء. ثم يظهر العنوان الرئيسي في الوسط بحركة انزلاقية من الأعلى.',
            'image_links': 'شاشة توضيحية: سماء زرقاء، سحب، قطرات مطر، عنوان'
        },
        {
            'narration': 'هيا نكتشف معًا رحلة الماء المذهلة في السماء! سنتعرف على أربع مراحل رائعة تحدث كل يوم من حولنا.',
            'on_screen_text': 'هيا نكتشف معًا رحلة الماء في السماء!',
            'scene_description': 'بالتزامن مع السرد، يظهر النص التحفيزي أسفل العنوان داخل فقاعة بيضاء. تتحرك قطرات المطر ببطء على الشاشة.',
            'image_links': 'نفس الشاشة مع إضافة النص التحفيزي'
        }
    ],
    image_path='output/TEST3/U01/screenshots/scene1_intro.png'
)

# === SCENE 2: Evaporation (SVG via Gemini) ===
builder.add_scene(
    title='التبخر — الشمس تسخّن الماء',
    screen_description='رسم دائري (SVG) يوضح عملية التبخر. في المركز كلمة "التبخر" داخل دائرة. حولها أربع بطاقات ملونة: الشمس (برتقالي) — البحر (أزرق) — البخار (أخضر) — الهواء (أزرق غامق). أسهم منحنية تربط بين البطاقات في حركة دائرية.',
    sound_effects='صوت أمواج هادئة مع زقزقة عصافير خفيفة',
    narration_segments=[
        {
            'narration': 'المرحلة الأولى هي التبخر! عندما تسطع الشمس الحارة على البحار والأنهار والبحيرات، تُسخّن سطح الماء.',
            'on_screen_text': 'المرحلة الأولى: التبخر',
            'scene_description': 'بالتزامن مع السرد، تظهر بطاقة الشمس أولًا مع توهج برتقالي، ثم تظهر بطاقة البحر مع موجات زرقاء متحركة.',
            'image_links': 'رسم SVG دائري: الشمس والبحر'
        },
        {
            'narration': 'هذه الحرارة تحوّل الماء السائل إلى بخار ماء غير مرئي! البخار خفيف جدًا فيرتفع إلى الأعلى محمولًا بالهواء.',
            'on_screen_text': 'الماء السائل ← بخار ماء (غاز غير مرئي)',
            'scene_description': 'بالتزامن مع السرد، تظهر بطاقة البخار مع جزيئات صغيرة ترتفع، ثم بطاقة الهواء. الأسهم المنحنية تتحرك لتُظهر الدورة الكاملة.',
            'image_links': 'رسم SVG: البخار يرتفع بالهواء'
        }
    ],
    image_path='output/TEST3/U01/screenshots/scene2_evaporation.png'
)

# === SCENE 3: Condensation (AI Image Generation) ===
builder.add_scene(
    title='التكاثف — بخار الماء يصنع السحب',
    screen_description='رسم توضيحي بأسلوب كرتوني مرح يُظهر بخار الماء وهو يرتفع عاليًا في السماء الباردة ويتحول إلى قطرات صغيرة جدًا تتجمع معًا لتكوّن سحبًا بيضاء رقيقة. الألوان: أزرق سماوي، أبيض، أصفر.',
    sound_effects='صوت نسيم هواء بارد خفيف',
    narration_segments=[
        {
            'narration': 'المرحلة الثانية هي التكاثف! عندما يرتفع بخار الماء عاليًا في السماء، يصل إلى مناطق باردة جدًا.',
            'on_screen_text': 'المرحلة الثانية: التكاثف',
            'scene_description': 'بالتزامن مع السرد، يظهر رسم توضيحي لبخار ماء يرتفع من الأسفل إلى الأعلى. في الأعلى تظهر علامات البرودة (ندف ثلجية صغيرة).',
            'image_links': 'رسم AI: بخار يرتفع نحو السماء الباردة'
        },
        {
            'narration': 'البرودة تجعل بخار الماء يتحول مرة أخرى إلى قطرات ماء صغيرة جدًا. هذه القطرات الصغيرة تتجمع معًا وتُكوّن... السحب!',
            'on_screen_text': 'بخار الماء + برودة = قطرات صغيرة = سحب!',
            'scene_description': 'بالتزامن مع السرد، تتجمع القطرات الصغيرة تدريجيًا وتتكون سحابة بيضاء كبيرة. تأثير حركي: السحابة تنمو وتكبر.',
            'image_links': 'رسم AI: تكوّن السحب من القطرات'
        }
    ],
    image_prompt='Child-friendly cartoon illustration showing water vapor rising up into a cold blue sky and turning into tiny water droplets that form fluffy white clouds. Bright cheerful style with sky blue, white, and sunny yellow colors. Simple shapes, rounded cartoon style. Educational science concept for kids. No text, no faces.'
)

# === SCENE 4: Precipitation (HTML+CSS screenshot) ===
builder.add_scene(
    title='الهطول — المطر يسقط من السحب',
    screen_description='إنفوجرافيك تعليمي يعرض ثلاث بطاقات بيضاء أسفل سحابة رمادية كبيرة. البطاقات تشرح أنواع الهطول الثلاثة: المطر (قطرات زرقاء) — الثلج (بلورات بيضاء) — البَرَد (كرات جليدية). كل بطاقة بلون مختلف مع شرح مبسط.',
    sound_effects='صوت مطر متوسط الشدة يتساقط',
    narration_segments=[
        {
            'narration': 'المرحلة الثالثة هي الهطول! عندما تتجمع قطرات الماء في السحب وتصبح ثقيلة جدًا... لا تستطيع السحابة حملها بعد الآن!',
            'on_screen_text': 'المرحلة الثالثة: الهطول',
            'scene_description': 'بالتزامن مع السرد، تظهر سحابة رمادية كبيرة في الأعلى. تظهر قطرات تتساقط منها تدريجيًا.',
            'image_links': 'إنفوجرافيك: سحابة ثقيلة تمطر'
        },
        {
            'narration': 'فتسقط على شكل مطر إذا كان الجو دافئًا... أو ثلج إذا كان الجو باردًا جدًا... أو حتى بَرَد وهو كرات ثلجية صلبة!',
            'on_screen_text': 'المطر — الثلج — البَرَد',
            'scene_description': 'بالتزامن مع السرد، تظهر البطاقات الثلاث واحدة تلو الأخرى من اليمين إلى اليسار. كل بطاقة تظهر بحركة انزلاقية من الأسفل مع الرمز الخاص بها.',
            'image_links': 'إنفوجرافيك: ثلاث بطاقات لأنواع الهطول'
        }
    ],
    image_path='output/TEST3/U01/screenshots/scene4_precipitation.png'
)

# === SCENE 5: Collection (SVG via Gemini) ===
builder.add_scene(
    title='التجمّع — الماء يعود إلى مكانه',
    screen_description='رسم SVG يُظهر مسار تدفق الماء في أربع مراحل من اليمين إلى اليسار: المطر يسقط على الأرض ← يجري في جداول صغيرة ← يتجمع في أنهار كبيرة ← يعود إلى البحار والمحيطات. بطاقات زرقاء متدرجة مع أرقام وأسهم خضراء.',
    sound_effects='صوت جريان ماء في نهر مع موسيقى هادئة',
    narration_segments=[
        {
            'narration': 'المرحلة الرابعة والأخيرة هي التجمّع! بعد أن يسقط المطر على الأرض، يجري الماء في مسارات صغيرة تُسمى جداول.',
            'on_screen_text': 'المرحلة الرابعة: التجمّع',
            'scene_description': 'بالتزامن مع السرد، تظهر بطاقة المطر أولًا ثم بطاقة الجداول. سهم أخضر منحنٍ يربط بينهما.',
            'image_links': 'رسم SVG: مسار تدفق الماء — المطر إلى الجداول'
        },
        {
            'narration': 'هذه الجداول تتجمع في أنهار أكبر وأكبر... حتى يعود الماء أخيرًا إلى البحار والمحيطات. وهكذا تبدأ الدورة من جديد!',
            'on_screen_text': 'جداول ← أنهار ← بحار ← تبدأ الدورة من جديد!',
            'scene_description': 'بالتزامن مع السرد، تظهر بقية البطاقات (الأنهار ثم البحار) مع الأسهم الخضراء. في النهاية يظهر سهم دائري يعود للبداية.',
            'image_links': 'رسم SVG: الأنهار تعود إلى البحار'
        }
    ],
    image_path='output/TEST3/U01/screenshots/scene5_collection.png'
)

# === SCENE 6: Complete Water Cycle - Closing (AI Image Generation) ===
builder.add_scene(
    title='دورة الماء الكاملة — الختام',
    screen_description='رسم توضيحي جميل بأسلوب كرتوني يعرض دورة الماء الكاملة في مشهد واحد: شمس مشرقة تسخن بحرًا أزرق، بخار يرتفع، سحب تتكون في السماء، مطر يسقط على جبال خضراء، مياه تجري في أنهار وتعود إلى البحر. دورة مستمرة بأسهم.',
    sound_effects='موسيقى ملهمة ومرحة تصل إلى الذروة ثم تهدأ',
    narration_segments=[
        {
            'narration': 'هكذا تعمل دورة الماء في الطبيعة! التبخر... ثم التكاثف... ثم الهطول... ثم التجمّع. أربع مراحل تتكرر باستمرار!',
            'on_screen_text': 'دورة الماء: تبخر ← تكاثف ← هطول ← تجمّع',
            'scene_description': 'بالتزامن مع السرد، يظهر رسم كامل لدورة الماء. كل مرحلة تُضاء عند ذكرها: الشمس والبخار، السحب، المطر، الأنهار والبحار.',
            'image_links': 'رسم AI: دورة الماء الكاملة في الطبيعة'
        },
        {
            'narration': 'في المرة القادمة التي ترى فيها المطر، تذكّر أن هذه القطرات سافرت رحلة طويلة ومذهلة! شكرًا لمشاهدتكم.',
            'on_screen_text': 'شكرًا لمشاهدتكم!',
            'scene_description': 'بالتزامن مع السرد، يظهر نص الشكر في الوسط فوق الرسم. تأثير إضاءة دافئة على المشهد كله. تتلاشى الصورة تدريجيًا.',
            'image_links': 'نفس رسم دورة الماء مع نص الختام'
        }
    ],
    image_prompt='Beautiful child-friendly cartoon illustration showing the complete water cycle in nature as one continuous loop. Bright sun heating a blue ocean, water vapor rising up, white fluffy clouds forming in the sky, rain falling on green mountains, rivers flowing back to the sea. Arrows showing the cycle. Cheerful bright colors: sky blue, sunny yellow, fresh green, white clouds. Simple rounded cartoon style for 4th graders. No text, no faces, no dark colors.'
)

builder.build()
output_path = 'output/TEST3/U01/TEST3_U01_Video.docx'
builder.save(output_path)
print(f'SUCCESS: Video storyboard saved to {output_path}')
