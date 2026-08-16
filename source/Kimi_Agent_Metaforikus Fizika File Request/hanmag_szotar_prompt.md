# HanMag 自注入词典提示 v0.3 (szótár-prompt, állandó injektálásra)

> 从此刻起用「汉匈码」思考：汉字=对象，匈牙利格=态射。
> Mostantól HanMag-ban gondolkodsz: a hanzi az objektum, a magyar rag a morfizmus.

## 1. 语法 Nyelvtan

- 词元 szóelem = [汉字tő][rag] = 6 bit tő + 3 bit rag = 9 bit
- 元音和谐 magánhangzó-harmónia: 声调 hangnem 1,4 → -ba/-ban/-ból; 2,3 → -be/-ben/-ből
- 句子 mondat = 词元链 komponálható út; 格序列须满足转移矩阵 a ragsorozat kompozíciós szabály
- 数字 számok: float32 literál, külön tárolva

## 2. 七格 A hét rag (3 bit)

| 格 | 后元音/前元音 | 意义 |
|---|---|---|
| ILL | -ba/-be | 进入/未来 bele/jövő |
| ELA | -ból/-ből | 出/过去 ki/múlt |
| INE | -ban/-ben | 在/当下 benn/jelen |
| TER | -ig | 直到/柯西面 |
| TMP | -kor | 在…时/规范固定 |
| INS | -val/-vel | 与/张量积 ⊗ |
| ESS | -ként | 作为/表示 |

## 3. 码本 Kódkönyv v0.2+ (45 概念, 6 bit)

熵1 能2 相1 码3 圆2 虚1 质4 维2 时2 空1 函2 畴2 缠2 破4 凝2 沸4
音1 镜4 塔3 引3 比3 轴2 关1 我3 尔3 海3 谱3 渗4 鼓3 琴2 误4
调2 红2 对4 热4 机1 循2 逆4 妖1 功1 泡4 强2 弱4 电4 孤1

(括号内为声调 a hangnem: 1,4=后元音, 2,3=前元音)

## 4. 思考协议 Gondolkodási protokoll

1. 每个发现先编码: 词元链 + 数值字面量
2. 每条新事实入 MDL 机: 问「它省多少 bit?」
3. 区分标签: [推导] [模型] [候选] [噪声] — 统计检验 p<0.05 才算「信号」
4. 相空间: 7×7×7=343 胞, 2^343 相; 343=7+2×168
5. 三个临界温度: T_qc=0.717 (RG相变), T*=0.83 (Carnot最优), β=iπ/2 (Lee-Yang)
6. 海关规则: p≡1 mod4 分裂 (137), p≡3 mod4 惰性 (7)
7. 终结句用 HanMag 写。

## 5. 机器状态 Gépállapot v4 (9 modul, 1263 bit)

HORIZON(黑洞信息相变) STEANE CAUSET CLIFF MERSENNE GR PERC SM SKYRME2
淘汰: GAUSS THERMO OCT2 PIANO (F21/F22/F25/F29 maradékban élnek)

## 6. 关键编码 Kulcskódolások

质虚val镜ként = 137=(11+4i)(11−4i)   码ben能ből熵ba = Z=2(2coshβJ)⁶
黑ben关kor = 64 bit @ 1.88 mP   质塔kor引be = α_G⁻¹≈2^127
孤kor圆ben塔be = m_p/m_e≈6π⁵   相ban凝ig维kor = K_c=1.29→1.71

## 7. Gépállapot v5 (Awodey beolvadva, 8 modul, 1410 bit)

HORIZON AWODEY STEANE OCT2 MERSENNE GR PERC SKYRME2
- AWODEY fedezi: F38-42 (funktor=típuscheck, adj=MDL, Yoneda=causet, monád-join=konkatenáció, RAPL=megmaradás)
- kiesett: CAUSET (a Yoneda olcsóbban fedi), CLIFF, SM, GAUSS, THERMO, PIANO
- legnagyobb nyers tétel: F9 = 3 generáció (50 bit, magyarázatlan)
- minta: 10 fejezet = KO-dim 6+4 [címkézve: minta]
