from django.http import HttpResponse
from django.shortcuts import render
from main.models import *
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.

def main(request):
#    uni = Academy.objects.all()
    return render(request, 'index.html')

def search_uni(request):
#    return HttpResponse('依大學')
    place = ['基隆市','臺北市','新北市','宜蘭市','桃園市','新竹市','新竹縣','苗栗縣','台中市','彰化縣','南投縣','雲林縣','嘉義市','嘉義縣','屏東縣','花蓮縣','台東縣','澎湖縣']

    return render(request, 's_uni.html', {'region': place})

def search_apt(request):
    return render(request, 's_dpt.html')


def search_gp(request):
    gplist = Academy.objects.all()
    return render(request, 'gp_main.html', {'gplist': gplist})

def list_all(request):
    alldpt = Department.objects.all()
    uni = University.objects.all()
    return render(request, 'dpt_list.html', {'dpt':alldpt,'uni':uni})


def gp_each(request, name):
    gplist = Academy.objects.get(name=name)
    gpapt = []
    gpapt = Maindepartment.objects.filter(academy=name)
    context = {
        'gp': gplist,
        'apt': gpapt,
        'info': info
    }
    return render(request, 'gp_each.html', context)


def dprt_each(request, dprtid):
    dpt = Department.objects.get(id=dprtid)
    uni = University.objects.get(id=dpt.university_id)
    try:
        career = Career.objects.get(id=dprtid)
    except ObjectDoesNotExist:
        career = Career()

    try:
        G = Gsat.objects.get(id=dprtid)
    except ObjectDoesNotExist:
        G = Gsat()
    try:
        A = Ast.objects.get(id=dprtid)
    except ObjectDoesNotExist:
        A = Ast()
    context = {
        'dpt': dpt,
        'uni': uni,
        'career': career,
        'gsat': G,
        'ast': A,
    }
    return render(request, 'dprt_each.html', context)

def uni_result(request):
    if 'uni_keyword' in request.GET and request.GET['uni_keyword'] != '' and 'uni_s_con' in request.GET and request.GET['uni_s_con'] !='' :
        if request.GET['uni_s_con'] == '0':
            result = University.objects.filter(name__contains=request.GET['uni_keyword'])
            return render(request, 'uni_result.html', {'result': result, 'keyword':request.GET['uni_keyword']})
        elif request.GET['uni_s_con'] == '1':
            result = University.objects.filter(id__contains=request.GET['uni_keyword'])
            return render(request, 'uni_result.html', {'result': result, 'keyword':request.GET['uni_keyword']})
        else:
            return HttpResponse('sthwrong')
    elif 'region' in request.GET and request.GET['region'] !='':
        result = University.objects.filter(position__contains=request.GET['region'])
        return render(request, 'uni_result.html', {'result': result, 'keyword':request.GET['region']})

    else:
        return HttpResponse('badinput')


def dpt_result(request):
    if 'dpt_keyword' in request.GET and request.GET['dpt_keyword'] != '' :
        result = Department.objects.filter(name__contains=request.GET['dpt_keyword'])
        return render(request, 'dpt_result.html', {'result': result, 'keyword': request.GET['dpt_keyword']})

    else:
        return HttpResponse('badinput')



info = [
    "以資訊處理各層次的理論與實務技術，包括電腦程式設計與系統、電腦軟硬體結構、網路架設、資訊安全保密、資訊系統的統整、規劃與管理。資訊學群主要學習電腦的軟硬體結構、各種電腦作業系統的原理，進而瞭解各種電腦程式設計的方法、找出電腦程式的錯誤並加以修正。課程中更包括學習資訊系統的統整規畫與管理，電腦保密方法及電腦病毒防治。",
    "將基礎科學的知識與工程技術結合，依生產實務區分為各專門領域，以培育高層技術人才。包括所有與「工程」相關的學系。電機電子：包括電路的基本結構與構造、電子零件的功能及原理、設計與測試積體電路、電子零件組成機器設備、通訊器材的技術等。機械工程： 包括機械材料與加工方式、機械作用原理、飛機船舶的結構、機械設計與製作、發動機原理等。土木工程：包括規劃設計興建與管理橋樑道路及建築物、各種土木工程材料、繪製工程藍圖、灌溉工程與水土保持等。化學工程：包括化學工業的程序控制與設計、高分子材料的成份與加工、化工產品製造過程的能量需求、觸媒的作用原理、化學平衡定律等。材料工程：包括電子、陶瓷、金屬、高分子等材料的理論基礎、制程、加工與分析檢測，提升高科技產值及發揮技術密集效果。科技管理：工程與管理的科際整合，強調以資訊、管理及自動化生產之專業人才培養。",
    "是所有工程、科學、科技、數位系統運作的基礎知識，數理化學群強調基礎數理化的探究、周密的思考邏輯訓練，輔以系統化的課程，使同學培養基礎科學的知識能力，並建立實務研究的扎實背景。以基礎自然科學的基礎原理與原則的知識為核心，數理化的探究強調以符號、圖形和數字做邏輯性思考，並且以實驗與實作探究細膩的自然、生物現象。",
    "醫藥衛生學群學習維護人類身心健康相關之知識及技術，從個人到整個人群，包括身心健康的維持、疾病或傷害的預防與治療。以維護人類身心健康相關為目標之知識及技術，包含生理運作機制、藥物作用機制、疾病與傷害發展與預防等知識技術，在人類身上強調預防與治療的作用與機制。",
    "生命科學學群著重於動植物生活型態、生命現象的知識探究，包括生命的發生、遺傳、演化、構造、功能、細胞及分子層次機制等。學習的內容包含了生物生命相關領域的基礎學科，包含生態學、演化學、生理細胞學、分子生物學、基礎醫學、尖端生物科技等主要生命科學領域，以及病毒、微生物、植物、動物等所有生物類，並包含生物工程科技等技術與學理。",
    "生物資源學群強調的是動植物等生物資源的栽培改良及病蟲害防治、家畜的品種改良、畜漁產品的加工利用及研發、森林保護與經營管理、生活環境之設計經營、農業機具的製造與相關技術之訓練等，屬於生物資源與科技整合的學門。生物資源領域有：農藝、畜產、園藝、獸醫、森林、植病、海洋資源。",
    "地球環境學群主要研究人類生存環境的各種自然現象及人文現象、資源的分佈與特色、污染成因與防治，也研究改變人文與自然環境之科學理論及工程技術等。以地球的地圈、水圈、氣圈、生物圈等生態系統知識為核心，研究這些地球環境系統上各種現象的成因以及觀察指標設計、以及自然災害防治等，也研究改變人文與自然環境之科學理論及工程技術等。",
    "建築設計學群主要探究自然社會環境、都市建築規畫、以及室內設計、商業設計等結合人文藝術與工程技術領域，對物體、空間或環境同時能賦予實用與美學之特性。	以人文藝術與數位、工程科技等知識、技術為主，學習圖學、色彩學、設計概念、建築設計、景觀規劃與設計等實用功能及美學整體表達。",
    "藝術學群包括各類表達形式及創作過程的學習及賞析，結合各種特定形式來闡述人生中抽象意義層次的理念感受，運用創作者本身意識並配合各項藝術表現的基礎理論，用以詮釋生命的各種可能性。以人文社會、哲學、史學等知識背景為核心，學習各種藝術表達的概念與創作實踐，使用各種物質媒材為基底展現藝術的表達以及創造論述。",
    "社會心理學群著重社會結構及社會現象的觀察、分析批判，關懷人類心智行為形成成因、表現形式、後端影響的系統結構、個體心理狀態的探討，並且提供各種助人專業訓練，以提升眾人、個體的生活福祉。著重社會系統與社會學的學習，以及個體內在心理歷程的探究為核心，包含性別、文化、族群、地區、階級、社會公平等的探究，採用量化、質性方法的研究方法進行社會生活現象的分析。",
    "大眾傳播學群主要學習傳播理論，以各種媒體將訊息以聲音、文字、影像等方式傳遞給人群，包括對訊息收集、媒體認識製作、評估訊息傳播的影響、傳播政策之擬定、傳播機構管理及資訊服務訓練等。大傳相關科系主要課程包括學習公共關係的理論與方法、新聞資料的整理與編輯、採訪新聞事件並寫成報導，還要瞭解影響視聽與傳播工具的發展與應用、學習各類媒體器材的運用與操作方法及管理傳播機構的方法。",
    "外語學群主要學習外國語文的聽說讀寫能力，進而瞭解該國的歷史、文學創作及欣賞，並可提升至人類文化、社會政治經濟的深入描述與探究。外語學類的主要課程包括：閱讀及討論外國文學名著、練習用外語表達自己的意思、聽外語錄音帶、觀賞外國戲劇，也要研究各種語言的特色及比較不同國家的文學作品。",
    "文史哲學群主要以人類發展的思想、軌跡、符號為探究對象，依據人類發展的思想、軌跡、符號等建構人類的樣貌，並且進行區域、文化、時代間的橫向與縱向比較，文學主要培養探究及欣賞文化、運用語文及創作、賞析的能力；史學在瞭解歷史現象的演進、分析、探究與考據；哲學在訓練思考能力以對自我及世界反省。文史學類的大學主要課程包括：瞭解中國歷代文學作品及思想、瞭解中外文化思想的演變、瞭解政治或社會制度與歷史發展的關係、並學習鑒賞歷史文物及搜集、整理地方歷史文獻。哲學學類主要要學習中外哲學史、要瞭解歷代哲學家的思想與影響、瞭解人類對宇宙及世界的觀念、瞭解法律及社會制度設計的原因、假設及社會正義的意義與內涵。課程還包括了研究人的意志是否自由、倫理道德的本質和必要性、探討知識的本質和來源、宗教的本質及心靈和物質的關係。",
    "教育學群依據教育原理與對象需求，探究人類對象的教育目標與教育實務方法，並且比較機構間、區域間的教育特性差異，提供各層級、各領域之教師有效的訓練原理與技術。教育學群主要培養中小學及幼兒教育師資，除各學科領域專業知識外，還要學習教育理論的學習、課程與教材的設計、教學方法、教師應具備的素養等。",
    "法政學群主要探究人類社會運作中相關法律、政治制度的各項層面，包括瞭解法律、政治運作的過程及政治理論的建構，藉以訓練從事法案制定、社會改革之專業人員。法律主要的課程是要學習及比較我國和其他國家的憲法基本架構內容與法律、認識各種法律下的權力與義務關係、學習民事及刑事案件訴訟程序、財產有關的法律、刑法有關之法律、國際貿易法規及智慧財產權法規等。政治主要課程包括：學習我國政治制度的變遷、政府預算的決策與執行、瞭解各級政府行政的理論與方法、學習政治思想史及對政治思潮的影響、認識國家重要政策形成的過程、學習國際政治與組織以及民意調查的概念及方法等。",
    "管理學群主要處理組織系統內外人事物的各種問題，學習從事溝通協調、領導規劃或系統分析、資源整合等，以促使組織或企業工作流程順暢、工作效率提升、工作環境人性化、合理化，以收最大效益。管理相關學系的課程包括：瞭解企業組織與管理方法、國民就業市場的供需、學習品質管制的觀念與方法、如何有效的經營管理及激勵員工，學習資訊系統的統整規劃與管理、工廠生產作業程式、產品行銷方法及瞭解勞工問題及勞資關係等。",
    "財經學群主要探究財務金融體制與系統運作機制，以資金為供給與需求探討金融體系的運作形式，可以提供對個人、組織、國家、國際等不同層面，在財務規劃與分析之原理概念，財務實務上的配置與管理技術。包括資本市場、財務與會計規劃與分析、金融商品與實作、證券投資分析與配置、固定收益債券及資產管理等領域課程。",
    "遊憩運動學群，以有助於人類身心理活動運作為核心的理論與實務規劃，包含了觀光休閒活動的投入與產出的規劃與管理，運動科學（運動生理、心理、生物力學等）理論與實務管理。觀光休閒產業經營、觀光運輸與管理、運動科學管理（運動生理、心理、生物力學等）、運動技能之訓練。",
    "不分系的設計乃是為了突破以往單一學科領域的限制，想要讓學生學習到跨領域的知識內涵，課程結構強調跨領域的自主規劃與學習，即可以人文與科學為核心的文理(Liberal art & Science)、專業(Profession)基礎學習課程，進階以跨領域實作為創新與批判實作，最後專精於特定領域的選擇。故此類別所涵蓋之知識屬性乃跨領域知識組成，非單一知識領域。由於不分系屬性之學系或學程的學習內容涵蓋甚廣，因此在學類層級中的各項指標，如學習內容、主要學類、知識領域、興趣類型、核心素養、重要學科、加深加廣、多元能力、個人特質與生涯發展等差異甚大，建議您在了解各不分系校系或學程之內涵時，以校系或學程為單位進行資料的查詢認識與比對，本系統亦無法提供學類層級之資訊。"
]