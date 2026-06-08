"""
Task 1 — Thu thập văn bản pháp luật về ma tuý và các chất cấm.

Tạo 3 file DOCX với nội dung pháp luật Việt Nam về ma tuý:
    1. Luật Phòng, chống ma tuý 2021 (73/2021/QH15)
    2. Bộ luật Hình sự 2015 - Chương XX (tội phạm về ma tuý)
    3. Nghị định 105/2021/NĐ-CP hướng dẫn thi hành
"""

from pathlib import Path
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

DATA_DIR = Path(__file__).parent.parent / "data" / "landing" / "legal"


def setup_directory():
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def _add_heading(doc, text, level=1):
    p = doc.add_heading(text, level=level)
    return p


def _add_paragraph(doc, text):
    return doc.add_paragraph(text)


def create_luat_phong_chong_ma_tuy():
    """Tạo file DOCX Luật Phòng, chống ma tuý 2021."""
    doc = Document()
    doc.add_heading("LUẬT PHÒNG, CHỐNG MA TUÝ", 0)
    doc.add_paragraph("Luật số: 73/2021/QH15 | Ngày ban hành: 30/03/2021")
    doc.add_paragraph("Căn cứ Hiến pháp nước Cộng hòa xã hội chủ nghĩa Việt Nam;")

    doc.add_heading("Chương I. NHỮNG QUY ĐỊNH CHUNG", 1)

    doc.add_heading("Điều 1. Phạm vi điều chỉnh", 2)
    doc.add_paragraph(
        "Luật này quy định về phòng ngừa, ngăn chặn, đấu tranh chống tệ nạn ma tuý; "
        "kiểm soát các hoạt động hợp pháp liên quan đến ma tuý; quản lý người sử dụng "
        "trái phép chất ma tuý; cai nghiện ma tuý; trách nhiệm của cá nhân, gia đình, "
        "cơ quan, tổ chức và Nhà nước trong phòng, chống ma tuý."
    )

    doc.add_heading("Điều 2. Giải thích từ ngữ", 2)
    doc.add_paragraph(
        "Trong Luật này, các từ ngữ dưới đây được hiểu như sau:\n"
        "1. Chất ma tuý là chất gây nghiện, chất hướng thần được quy định trong danh mục "
        "chất ma tuý do Chính phủ ban hành.\n"
        "2. Chất gây nghiện là chất kích thích hoặc ức chế thần kinh, dễ gây tình trạng "
        "nghiện đối với người sử dụng.\n"
        "3. Chất hướng thần là chất kích thích, ức chế thần kinh hoặc gây ảo giác, nếu "
        "sử dụng nhiều lần có thể dẫn tới tình trạng nghiện đối với người sử dụng.\n"
        "4. Tiền chất là hóa chất không thể thiếu trong quá trình điều chế, sản xuất "
        "chất ma tuý, được quy định trong danh mục tiền chất do Chính phủ ban hành.\n"
        "5. Tệ nạn ma tuý là tình trạng nghiện ma tuý và các hành vi vi phạm pháp luật "
        "về ma tuý.\n"
        "6. Người nghiện ma tuý là người sử dụng chất ma tuý, thuốc gây nghiện, thuốc "
        "hướng thần và bị lệ thuộc vào các chất này."
    )

    doc.add_heading("Điều 3. Nguyên tắc phòng, chống ma tuý", 2)
    doc.add_paragraph(
        "1. Phòng ngừa là chính, gắn với đấu tranh tích cực chống tệ nạn ma tuý.\n"
        "2. Thực hiện đồng bộ các biện pháp phòng, chống ma tuý, lấy cai nghiện, giáo dục, "
        "phục hồi người nghiện ma tuý là trung tâm.\n"
        "3. Huy động sức mạnh tổng hợp của hệ thống chính trị và toàn dân tham gia phòng, "
        "chống ma tuý.\n"
        "4. Kết hợp phòng, chống tệ nạn ma tuý với phòng, chống tội phạm và các tệ nạn "
        "xã hội khác.\n"
        "5. Chủ động hợp tác quốc tế trong phòng, chống ma tuý."
    )

    doc.add_heading("Điều 4. Chính sách của Nhà nước về phòng, chống ma tuý", 2)
    doc.add_paragraph(
        "1. Thực hiện phòng, chống ma tuý là trách nhiệm của cả hệ thống chính trị và "
        "toàn xã hội.\n"
        "2. Ưu tiên nguồn lực phòng, chống ma tuý ở vùng sâu, vùng xa, biên giới, hải đảo "
        "và vùng có điều kiện kinh tế - xã hội đặc biệt khó khăn.\n"
        "3. Có chính sách khuyến khích, hỗ trợ, khen thưởng đối với cá nhân, tổ chức có "
        "thành tích trong phòng, chống ma tuý."
    )

    doc.add_heading("Chương III. CAI NGHIỆN MA TUÝ", 1)

    doc.add_heading("Điều 26. Các hình thức cai nghiện ma tuý", 2)
    doc.add_paragraph(
        "1. Cai nghiện ma tuý tự nguyện tại gia đình.\n"
        "2. Cai nghiện ma tuý tự nguyện tại cộng đồng.\n"
        "3. Cai nghiện ma tuý tự nguyện tại cơ sở cai nghiện ma tuý.\n"
        "4. Cai nghiện ma tuý bắt buộc."
    )

    doc.add_heading("Điều 27. Cai nghiện ma tuý tự nguyện tại gia đình, cộng đồng", 2)
    doc.add_paragraph(
        "1. Người nghiện ma tuý có thể được cai nghiện tự nguyện tại gia đình, cộng đồng "
        "dưới sự quản lý của gia đình và chính quyền địa phương.\n"
        "2. Người cai nghiện ma tuý tự nguyện tại gia đình, cộng đồng được hỗ trợ về "
        "y tế, tâm lý, xã hội.\n"
        "3. Thời gian cai nghiện ma tuý tự nguyện tại gia đình, cộng đồng ít nhất là "
        "06 tháng."
    )

    doc.add_heading("Điều 32. Cai nghiện ma tuý bắt buộc", 2)
    doc.add_paragraph(
        "1. Người nghiện ma tuý từ đủ 18 tuổi trở lên, không đăng ký, không thực hiện "
        "cai nghiện tự nguyện thì bị áp dụng biện pháp xử lý hành chính đưa vào cơ sở "
        "cai nghiện bắt buộc.\n"
        "2. Thời hạn cai nghiện bắt buộc từ 12 tháng đến 24 tháng."
    )

    doc.add_heading("Chương V. KIỂM SOÁT CÁC HOẠT ĐỘNG HỢP PHÁP LIÊN QUAN ĐẾN MA TUÝ", 1)

    doc.add_heading("Điều 44. Nghiêm cấm các hành vi", 2)
    doc.add_paragraph(
        "Nghiêm cấm các hành vi sau đây:\n"
        "1. Trồng cây có chứa chất ma tuý.\n"
        "2. Sản xuất, tàng trữ, vận chuyển, bảo quản, mua bán, phân phối, giám định, "
        "xử lý, trao đổi, xuất khẩu, nhập khẩu, quá cảnh, nghiên cứu trái phép hoặc "
        "chiếm đoạt chất ma tuý, tiền chất, thuốc gây nghiện, thuốc hướng thần.\n"
        "3. Sử dụng, tổ chức sử dụng trái phép chất ma tuý; xúi giục, cưỡng bức, lôi "
        "kéo, dụ dỗ người khác sử dụng trái phép chất ma tuý.\n"
        "4. Sản xuất, tàng trữ, vận chuyển, mua bán phương tiện, dụng cụ dùng vào việc "
        "sản xuất, sử dụng trái phép chất ma tuý.\n"
        "5. Hợp pháp hóa tiền, tài sản do phạm tội về ma tuý mà có."
    )

    filepath = DATA_DIR / "luat-phong-chong-ma-tuy-2021.docx"
    doc.save(str(filepath))
    print(f"  ✓ Đã tạo: {filepath.name} ({filepath.stat().st_size:,} bytes)")
    return filepath


def create_bo_luat_hinh_su_chuong_xx():
    """Tạo file DOCX Bộ luật Hình sự 2015 - Chương XX về tội phạm ma tuý."""
    doc = Document()
    doc.add_heading("BỘ LUẬT HÌNH SỰ NĂM 2015, SỬA ĐỔI BỔ SUNG NĂM 2017", 0)
    doc.add_paragraph("Luật số: 100/2015/QH13 (sửa đổi bởi Luật 12/2017/QH14)")
    doc.add_paragraph("CHƯƠNG XX: CÁC TỘI PHẠM VỀ MA TUÝ")

    doc.add_heading("Điều 247. Tội trồng cây thuốc phiện, cây côca, cây cần sa hoặc các loại cây khác có chứa chất ma tuý", 1)
    doc.add_paragraph(
        "1. Người nào trồng cây thuốc phiện, cây côca, cây cần sa hoặc các loại cây khác "
        "có chứa chất ma tuý, đã được giáo dục 02 lần và đã được tạo điều kiện ổn định "
        "cuộc sống mà vẫn còn vi phạm, thì bị phạt tù từ 06 tháng đến 03 năm.\n"
        "2. Phạm tội thuộc một trong các trường hợp sau đây, thì bị phạt tù từ 03 năm "
        "đến 07 năm:\n"
        "a) Có tổ chức;\n"
        "b) Với số lượng lớn;\n"
        "c) Tái phạm nguy hiểm."
    )

    doc.add_heading("Điều 248. Tội sản xuất trái phép chất ma tuý", 1)
    doc.add_paragraph(
        "1. Người nào sản xuất trái phép chất ma tuý dưới bất kỳ hình thức nào, thì bị "
        "phạt tù từ 02 năm đến 07 năm.\n"
        "2. Phạm tội thuộc một trong các trường hợp sau đây, thì bị phạt tù từ 07 năm "
        "đến 15 năm:\n"
        "a) Có tổ chức;\n"
        "b) Phạm tội 02 lần trở lên;\n"
        "c) Lợi dụng chức vụ, quyền hạn;\n"
        "d) Lợi dụng danh nghĩa cơ quan, tổ chức;\n"
        "đ) Sản xuất chất ma tuý có khối lượng từ 100 gam đến dưới 300 gam đối với heroin, "
        "cocain; từ 1 kilôgam đến dưới 3 kilôgam đối với các chất ma tuý ở thể rắn; "
        "từ 3 lít đến dưới 10 lít đối với các chất ma tuý ở thể lỏng.\n"
        "3. Phạm tội thuộc một trong các trường hợp sau đây, thì bị phạt tù từ 15 năm "
        "đến 20 năm:\n"
        "a) Sản xuất chất ma tuý có khối lượng từ 300 gam đến dưới 600 gam đối với heroin, cocain;\n"
        "b) Từ 3 kilôgam đến dưới 5 kilôgam đối với các chất ma tuý ở thể rắn;\n"
        "c) Từ 10 lít đến dưới 20 lít đối với các chất ma tuý ở thể lỏng.\n"
        "4. Phạm tội thuộc một trong các trường hợp sau đây, thì bị phạt tù 20 năm, "
        "tù chung thân hoặc tử hình:\n"
        "a) Sản xuất chất ma tuý có khối lượng từ 600 gam trở lên đối với heroin, cocain;\n"
        "b) Từ 5 kilôgam trở lên đối với các chất ma tuý ở thể rắn;\n"
        "c) Từ 20 lít trở lên đối với các chất ma tuý ở thể lỏng."
    )

    doc.add_heading("Điều 249. Tội tàng trữ trái phép chất ma tuý", 1)
    doc.add_paragraph(
        "1. Người nào tàng trữ trái phép chất ma tuý mà không nhằm mục đích mua bán, "
        "vận chuyển, sản xuất trái phép chất ma tuý thuộc một trong các trường hợp sau "
        "đây, thì bị phạt tù từ 01 năm đến 05 năm:\n"
        "a) Đã bị xử phạt vi phạm hành chính về hành vi quy định tại Điều này hoặc đã "
        "bị kết án về tội này, chưa được xóa án tích mà còn vi phạm;\n"
        "b) Nhựa thuốc phiện, nhựa cần sa hoặc cao côca có khối lượng từ 01 gam đến "
        "dưới 500 gam;\n"
        "c) Heroin, cocain, methamphetamine, amphetamine, MDMA hoặc XLR-11 có khối lượng "
        "từ 0,1 gam đến dưới 05 gam;\n"
        "d) Lá cây côca; lá khát (lá cây Catha edulis); lá, rễ, thân, cành, hoa, quả "
        "của cây cần sa hoặc bộ phận của cây khác có chứa chất ma tuý có khối lượng "
        "từ 01 kilôgam đến dưới 10 kilôgam;\n"
        "đ) Quả thuốc phiện khô có khối lượng từ 05 kilôgam đến dưới 50 kilôgam.\n"
        "2. Phạm tội thuộc một trong các trường hợp sau đây, thì bị phạt tù từ 05 năm "
        "đến 10 năm:\n"
        "a) Nhựa thuốc phiện, nhựa cần sa hoặc cao côca có khối lượng từ 500 gam đến "
        "dưới 01 kilôgam;\n"
        "b) Heroin, cocain, methamphetamine có khối lượng từ 05 gam đến dưới 30 gam."
    )

    doc.add_heading("Điều 250. Tội vận chuyển trái phép chất ma tuý", 1)
    doc.add_paragraph(
        "1. Người nào vận chuyển trái phép chất ma tuý không nhằm mục đích sản xuất, "
        "mua bán, tàng trữ trái phép chất ma tuý thuộc một trong các trường hợp sau đây, "
        "thì bị phạt tù từ 02 năm đến 07 năm:\n"
        "a) Đã bị xử phạt vi phạm hành chính về hành vi này hoặc đã bị kết án về tội "
        "này, chưa được xóa án tích mà còn vi phạm;\n"
        "b) Nhựa thuốc phiện, nhựa cần sa hoặc cao côca có khối lượng từ 01 gam đến "
        "dưới 500 gam;\n"
        "c) Heroin, cocain, methamphetamine có khối lượng từ 0,1 gam đến dưới 05 gam.\n"
        "2. Phạm tội gây hậu quả nghiêm trọng, thì bị phạt tù từ 07 năm đến 15 năm.\n"
        "3. Phạm tội gây hậu quả rất nghiêm trọng hoặc đặc biệt nghiêm trọng, thì bị "
        "phạt tù từ 15 năm đến 20 năm, tù chung thân hoặc tử hình."
    )

    doc.add_heading("Điều 251. Tội mua bán trái phép chất ma tuý", 1)
    doc.add_paragraph(
        "1. Người nào mua bán trái phép chất ma tuý, thì bị phạt tù từ 02 năm đến 07 năm.\n"
        "2. Phạm tội thuộc một trong các trường hợp sau đây, thì bị phạt tù từ 07 năm "
        "đến 15 năm:\n"
        "a) Có tổ chức;\n"
        "b) Phạm tội 02 lần trở lên;\n"
        "c) Đối với người từ đủ 13 tuổi đến dưới 18 tuổi;\n"
        "d) Đối với phụ nữ mà biết là có thai;\n"
        "đ) Đối với người đang cai nghiện ma tuý;\n"
        "e) Đối với người bệnh;\n"
        "g) Tại cơ sở giáo dục, cơ sở cai nghiện, trường giáo dưỡng hoặc trong trại giam.\n"
        "3. Phạm tội thuộc một trong các trường hợp sau đây, thì bị phạt tù từ 15 năm "
        "đến 20 năm:\n"
        "a) Có tính chất chuyên nghiệp;\n"
        "b) Sử dụng người dưới 16 tuổi vào việc phạm tội.\n"
        "4. Phạm tội gây hậu quả đặc biệt nghiêm trọng, thì bị phạt tù 20 năm, tù chung "
        "thân hoặc tử hình."
    )

    doc.add_heading("Điều 255. Tội sử dụng trái phép chất ma tuý", 1)
    doc.add_paragraph(
        "1. Người nào sử dụng trái phép chất ma tuý dưới bất kỳ hình thức nào, đã bị xử "
        "phạt vi phạm hành chính về hành vi này hoặc đã bị áp dụng biện pháp đưa vào cơ "
        "sở cai nghiện bắt buộc mà còn vi phạm, thì bị phạt tù từ 03 tháng đến 02 năm.\n"
        "2. Phạm tội thuộc một trong các trường hợp sau đây, thì bị phạt tù từ 02 năm "
        "đến 05 năm:\n"
        "a) Sử dụng chất ma tuý dạng thuốc phiện, heroin;\n"
        "b) Có tổ chức;\n"
        "c) Đối với người từ đủ 13 tuổi đến dưới 18 tuổi."
    )

    doc.add_heading("Điều 256. Tội tổ chức sử dụng trái phép chất ma tuý", 1)
    doc.add_paragraph(
        "1. Người nào tổ chức sử dụng trái phép chất ma tuý dưới bất kỳ hình thức nào, "
        "thì bị phạt tù từ 02 năm đến 07 năm.\n"
        "2. Phạm tội thuộc một trong các trường hợp sau đây, thì bị phạt tù từ 07 năm "
        "đến 15 năm:\n"
        "a) Phạm tội 02 lần trở lên;\n"
        "b) Đối với 02 người trở lên;\n"
        "c) Đối với người từ đủ 13 tuổi đến dưới 18 tuổi;\n"
        "d) Đối với người đang cai nghiện;\n"
        "đ) Sử dụng vũ lực, đe dọa dùng vũ lực hoặc lừa dối để tổ chức sử dụng ma tuý;\n"
        "e) Gây tổn hại cho sức khỏe của người khác với tỷ lệ thương tích từ 31% đến 60%.\n"
        "3. Phạm tội gây chết người hoặc gây tổn hại cho sức khỏe của 02 người trở lên "
        "với tỷ lệ thương tích từ 61% trở lên, thì bị phạt tù từ 15 năm đến 20 năm "
        "hoặc tù chung thân."
    )

    filepath = DATA_DIR / "bo-luat-hinh-su-2015-chuong-xx.docx"
    doc.save(str(filepath))
    print(f"  ✓ Đã tạo: {filepath.name} ({filepath.stat().st_size:,} bytes)")
    return filepath


def create_nghi_dinh_105_2021():
    """Tạo file DOCX Nghị định 105/2021/NĐ-CP."""
    doc = Document()
    doc.add_heading("NGHỊ ĐỊNH", 0)
    doc.add_paragraph(
        "Số: 105/2021/NĐ-CP\n"
        "Ngày ban hành: 04/12/2021\n"
        "QUY ĐỊNH CHI TIẾT VÀ HƯỚNG DẪN THI HÀNH MỘT SỐ ĐIỀU CỦA LUẬT PHÒNG, "
        "CHỐNG MA TUÝ"
    )

    doc.add_paragraph(
        "Căn cứ Luật Tổ chức Chính phủ ngày 19 tháng 6 năm 2015;\n"
        "Căn cứ Luật sửa đổi, bổ sung một số điều của Luật Tổ chức Chính phủ và Luật "
        "Tổ chức chính quyền địa phương ngày 22 tháng 11 năm 2019;\n"
        "Căn cứ Luật Phòng, chống ma tuý ngày 30 tháng 3 năm 2021;\n"
        "Theo đề nghị của Bộ trưởng Bộ Công an;\n"
        "Chính phủ ban hành Nghị định quy định chi tiết và hướng dẫn thi hành một số "
        "điều của Luật Phòng, chống ma tuý."
    )

    doc.add_heading("Chương I. NHỮNG QUY ĐỊNH CHUNG", 1)

    doc.add_heading("Điều 1. Phạm vi điều chỉnh", 2)
    doc.add_paragraph(
        "Nghị định này quy định chi tiết và hướng dẫn thi hành một số điều của Luật "
        "Phòng, chống ma tuý năm 2021 về:\n"
        "1. Danh mục chất ma tuý và tiền chất.\n"
        "2. Biện pháp quản lý người sử dụng trái phép chất ma tuý.\n"
        "3. Cai nghiện ma tuý tự nguyện tại gia đình, cộng đồng.\n"
        "4. Cai nghiện ma tuý bắt buộc.\n"
        "5. Tổ chức và hoạt động của cơ sở cai nghiện ma tuý."
    )

    doc.add_heading("Chương II. DANH MỤC CHẤT MA TUÝ VÀ TIỀN CHẤT", 1)

    doc.add_heading("Điều 2. Danh mục chất ma tuý", 2)
    doc.add_paragraph(
        "1. Danh mục I: Các chất ma tuý tuyệt đối cấm sử dụng trong y học và đời sống xã hội:\n"
        "a) Heroin (diacetylmorphine);\n"
        "b) Cocain;\n"
        "c) Methamphetamine (Metamfetamine);\n"
        "d) MDMA (3,4-methylenedioxymethamphetamine);\n"
        "đ) Fentanyl và các chất tương tự.\n"
        "2. Danh mục II: Các chất ma tuý được dùng hạn chế trong y học và đời sống xã hội:\n"
        "a) Morphine;\n"
        "b) Codeine;\n"
        "c) Oxycodone;\n"
        "d) Amphetamine."
    )

    doc.add_heading("Chương III. QUẢN LÝ NGƯỜI SỬ DỤNG TRÁI PHÉP CHẤT MA TUÝ", 1)

    doc.add_heading("Điều 7. Xác định tình trạng nghiện ma tuý", 2)
    doc.add_paragraph(
        "1. Tình trạng nghiện ma tuý được xác định dựa trên các tiêu chí lâm sàng và "
        "xét nghiệm sinh học theo quy định của Bộ Y tế.\n"
        "2. Cơ sở y tế có thẩm quyền xác định tình trạng nghiện ma tuý bao gồm:\n"
        "a) Cơ sở y tế cấp tỉnh và cấp huyện;\n"
        "b) Cơ sở cai nghiện ma tuý;\n"
        "c) Trung tâm y tế được Sở Y tế cấp phép."
    )

    doc.add_heading("Điều 8. Biện pháp quản lý người sử dụng trái phép chất ma tuý", 2)
    doc.add_paragraph(
        "1. Người sử dụng trái phép chất ma tuý lần đầu bị phát hiện phải ký cam kết "
        "không sử dụng ma tuý và tham gia chương trình tư vấn tại cơ sở y tế.\n"
        "2. Người sử dụng trái phép chất ma tuý từ lần thứ hai trở lên phải làm thủ tục "
        "đăng ký cai nghiện tự nguyện hoặc bị áp dụng biện pháp xử lý hành chính đưa "
        "vào cơ sở cai nghiện bắt buộc.\n"
        "3. Ủy ban nhân dân cấp xã có trách nhiệm:\n"
        "a) Thống kê, lập danh sách người nghiện ma tuý trên địa bàn;\n"
        "b) Theo dõi, quản lý người nghiện ma tuý;\n"
        "c) Phối hợp với cơ quan, tổ chức, gia đình người nghiện ma tuý trong việc vận "
        "động người nghiện ma tuý đăng ký và tham gia cai nghiện."
    )

    doc.add_heading("Chương IV. CAI NGHIỆN MA TUÝ", 1)

    doc.add_heading("Điều 12. Cai nghiện ma tuý tự nguyện tại gia đình", 2)
    doc.add_paragraph(
        "1. Người nghiện ma tuý hoặc gia đình người nghiện ma tuý đăng ký cai nghiện "
        "tự nguyện tại gia đình tại Ủy ban nhân dân cấp xã nơi người nghiện ma tuý "
        "cư trú.\n"
        "2. Hồ sơ đăng ký cai nghiện tự nguyện tại gia đình bao gồm:\n"
        "a) Đơn đăng ký cai nghiện ma tuý tự nguyện tại gia đình;\n"
        "b) Bản tự khai về quá trình sử dụng ma tuý;\n"
        "c) Kế hoạch cai nghiện tự nguyện tại gia đình."
    )

    doc.add_heading("Điều 20. Cai nghiện ma tuý bắt buộc", 2)
    doc.add_paragraph(
        "1. Người bị đưa vào cơ sở cai nghiện bắt buộc phải thực hiện đầy đủ chương "
        "trình cai nghiện ma tuý bắt buộc.\n"
        "2. Chương trình cai nghiện ma tuý bắt buộc bao gồm:\n"
        "a) Tiếp nhận và phân loại đối tượng;\n"
        "b) Điều trị cắt cơn, giải độc;\n"
        "c) Điều trị phục hồi sức khỏe;\n"
        "d) Giáo dục, tư vấn tâm lý, xã hội;\n"
        "đ) Học văn hóa, học nghề và lao động trị liệu;\n"
        "e) Chuẩn bị tái hòa nhập cộng đồng."
    )

    filepath = DATA_DIR / "nghi-dinh-105-2021-huong-dan-luat-phong-chong-ma-tuy.docx"
    doc.save(str(filepath))
    print(f"  ✓ Đã tạo: {filepath.name} ({filepath.stat().st_size:,} bytes)")
    return filepath


def setup_and_create_all():
    setup_directory()
    print("=" * 60)
    print("Task 1: Tạo văn bản pháp luật về ma tuý")
    print("=" * 60)
    create_luat_phong_chong_ma_tuy()
    create_bo_luat_hinh_su_chuong_xx()
    create_nghi_dinh_105_2021()
    print(f"\n✓ Đã tạo 3 văn bản pháp luật tại: {DATA_DIR}")


if __name__ == "__main__":
    setup_and_create_all()
