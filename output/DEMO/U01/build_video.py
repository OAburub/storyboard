import sys, os

_p = os.popen('git rev-parse --show-toplevel 2>/dev/null').read().strip() or os.getcwd()
sys.path.insert(0, os.path.join(_p, '.claude', 'skills', 'storyboard-generator', 'scripts'))
from docx_engine import VideoBuilder

img1 = os.path.join(_p, 'output', 'DEMO', 'U01', 'screenshots', '01_evaporation.png')
img2 = os.path.join(_p, 'output', 'DEMO', 'U01', 'screenshots', '02_condensation.png')
img3 = os.path.join(_p, 'output', 'NJR01', 'U01', 'images', 'rain_precipitation.png')

builder = VideoBuilder(
    project_code='DEMO',
    unit_number=1,
    unit_name='دورة المياه في الطبيعة',
    project_name='اختبار أدوات التصوير المرئي',
    institution='اختبار النظام',
    designer='النظام',
)
builder.set_element_name('فيديو موشن: كيف يتكوّن المطر؟')
builder.set_element_code('DEMO_U01_Video_Rain')

# Scene 1: التبخر — SVG rendered via Playwright
builder.add_scene(
    title='المشهد الأول: التبخُّر',
    screen_description='رسم توضيحي بتقنية SVG يُظهر الشمس تُسلّط أشعتها على سطح الماء، وفقاعات زرقاء تمثّل جزيئات البخار ترتفع تدريجياً نحو السماء. الخلفية تدرّج من الأزرق الداكن إلى الفاتح.',
    sound_effects='موسيقى هادئة — أصوات طبيعة خفيفة',
    narration_segments=[{
        'narration': 'تسخّن أشعة الشمس سطح الماء، فيتحوّل الماء إلى بخار خفيف يرتفع نحو السماء.',
        'on_screen_text': 'التبخُّر — تحوُّل الماء إلى بخار',
        'scene_description': 'تظهر الشمس في الزاوية العلوية اليمنى. خطوط متقطعة برتقالية تنزل من الشمس إلى سطح الماء. فقاعات زرقاء فاتحة تصعد في ثلاثة أعمدة متفاوتة الحجم. يظهر النص في إطار شبه شفاف.',
        'image_links': 'SVG مُنشأ بالكود — تصوير مرئي بـ Playwright | الأداة: screenshot_gen.py',
    }],
    image_path=img1,
)

# Scene 2: التكاثف — HTML Screenshot (science monitoring portal)
builder.add_scene(
    title='المشهد الثاني: التكاثُف',
    screen_description='شاشة توضيحية تحاكي بوابة رصد جوي علمية. واجهة داكنة تعرض لوحة إحصاءات (درجة الحرارة −5°م، ارتفاع 3200م، رطوبة 96%) وتصوراً مرئياً لمراحل تكوُّن السحاب من اليمين إلى اليسار.',
    sound_effects='صوت أمطار خفيفة في الخلفية',
    narration_segments=[{
        'narration': 'عندما يرتفع البخار ويبرد في الطبقات العليا من الغلاف الجوي، يتكاثف ويتحوّل إلى قطرات صغيرة تكوّن السحب.',
        'on_screen_text': 'التكاثُف — تحوُّل البخار إلى قطرات وسحاب',
        'scene_description': 'تُعرض واجهة المنصة بالكامل. تضيء البطاقات الأربع (بخار → تبريد → قطرات → سحابة) بالتسلسل مع تقدّم الراوي. أرقام الإحصاءات تُحدَّث ببطء.',
        'image_links': 'HTML + CSS — شاشة توضيحية مُصوَّرة بـ Playwright | الأداة: screenshot_gen.py',
    }],
    image_path=img2,
)

# Scene 3: التساقط — AI-generated (image_prompt, will attempt generation)
builder.add_scene(
    title='المشهد الثالث: التساقُط',
    screen_description='رسم توضيحي مُولَّد بالذكاء الاصطناعي: سحابة داكنة في الأعلى، وقطرات مطر زرقاء تتساقط على أرض خضراء مع تكوُّن بُرَك صغيرة. أسلوب رسومي هندسي بسيط.',
    sound_effects='صوت مطر واضح — قرع رعد بعيد',
    narration_segments=[{
        'narration': 'تتراكم القطرات في السحابة حتى تثقل، فتتساقط على شكل مطر يعود ليُرطّب الأرض من جديد.',
        'on_screen_text': 'التساقُط — عودة الماء إلى الأرض',
        'scene_description': 'تتساقط قطرات الماء من السحابة وتضرب الأرض الخضراء وتتكوّن البُرَك. في النهاية تُعرض دورة المياه الكاملة كمخطط دائري.',
        'image_links': 'صورة مُولَّدة بالذكاء الاصطناعي — Nano Banana Pro / Gemini 3 Pro',
    }],
    image_path=img3,
)

builder.build()
out_path = os.path.join(_p, 'output', 'DEMO', 'U01', 'DEMO_U01_Video_Rain.docx')
builder.save(out_path)
print('SAVED:', out_path)
