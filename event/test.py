# -*- coding: utf-8 -*-

def clean_text_list(input_list: list[str]) -> list[str]:
    result = []
    for item in input_list:
        cleaned_item = (
            item.replace('[', '')
                .replace(']', '')
                .replace('"', '')
                .replace(',', '')
                .strip()
        )
        if cleaned_item and len(cleaned_item) > 1:
            result.append(cleaned_item)
    return result

if __name__ == "__main__":
    # Dữ liệu đầu vào
    raw_data = ['[ ', '[ ', '" cổ bổn nhì quốc tín nghĩa quyển nhất đệ nhị đồng " , ', '" tặc hưu tẩu trương nhượng kiến sự cấp toại đầu hà nhi tử đế giữ trần lưu vương vị tri khó thật bất cảm cao thanh phục ở hà biên loạn thảo chi nội quân mã tứ tán khứ cản bất tri đí chi " , ', '" sở tại đế dữ vương phục chí tứ canh lộ thuỷ hựu hạ phúc trung cơ nỗi tương bão nhi khóc hựu phạ nhân tri giác thôn thanh thảo táng chi trung trần lưu vương viết thử gian bất khả cửu luyến tua biết " , ', '" đẳng hoạt lộ ở thị nhị nhân dĩ y tương kết tự thượng ngạn biên mãn địa kinh cức hắc ám chi trung bất kiến hành lộ chính vô nại hà hốt kiến lưu lao thiên bách thành còn quang mang vô diệu chỉ " , ', '" tại đế tiền phi chuyển trần lưu vương viết thử thiên trợ ngã huynh đệ dã toại tuỳ huỳnh hoả nhi hành tiệm tiệm kiến lộ hành chí ngũ canh túc thống bất năng hành sơn cương biên kiến nhứt thảo đôi đế giữ " , ', '" vương ngoạ ư thảo đôi chi trung thảo đôi tiền diện thị nhất sở trang viện trang chủ thị dạ mộng lưỡng hồng nhật dáng ở trang hậu kinh giác phi y xuất hộ tứ hạ quan vọng kiến trang hậu thảo đôi thượng " , ', '" hồng quang trong thiên hoảng mang vãng thị khước thị nhị nhân ngoạ ư thảo bạn trang chủ vấn vít nhị thiếu niên thuỳ gia chi tử đế bất cảm ứng trần lưu vương chỉ đế viết thử thị đương kim hoàng đế tao " , ', '" thập đương thị chi loạn đào nạn chí thử ngô nãi hoàng đệ trần lưu vương giả trang chủ đại kinh tái bái viết thần tiên triều tư đồ thôi liệt chi đệ thôi nghị dã nhân kiến thập thường thị mại quan tật " , ', '" tư cố ẩn ư thử toại phù tân nhập trang quỳ tiến tửu thực khước thuyết vấn cống cản thượng đoạn khuê nã chú vấn thiên tử hà tại khuê ngôn dĩ tại bán lộ tương thất bất tri hà vãng cống toại sát " , ', '" đoạn khuê ưng đầu ở mã hạng hạ phân binh tứ tán tìm cánh tự kỷ khước độc thừa nhất mã tuỳ lộ truy tìm ngẫu chí thôi nghị trang sát kiến thủ cấp vấn chi cống thuyết tường tới thôi nghị dẫn cống " , ', '" kiến đế khung thần thống khốc cống viết quốc bất khả nhất nhật vô quân thỉnh bệ hạ hoàn đô thôi hoạn trang thượng chỉ hữu xấu mã nhất thất bị giữ đế thừa cống dữ trần lưu vương cùng thừa nhất mã ly " , ', '" trang nhi hành bất đáo tam lý tư đồ vương doãn thái uý dương bưu tả quân hiệu uý thuần vu quỳnh hữu quân hiệu uý triệu manh hậu quân hiệu uý bào tín trung quân hiệu uý viên thiệu nhất hành nhân chúng " , ', '" sổ bách nhân mã tiếp trước xa giá quân thần giai khốc tiên sử nhân tướng đoạn khuê thủ cấp vãng kinh sư hiệu lệnh lánh hoán hảo mã dữ đế gặp trần lưu vương cưỡi toạ thốc đế hoàn kinh tiên thị lạc " , ', '" dương tiểu kiến dao viết đế phi đế vương phi vương thiên thặng vạn kỵ tẩu bắc mang chí thử quả ứng kỳ thức xe vì hành bất đáo sổ lý hốt kiến tinh kỳ tô nhật ma thổ già thiên nhất chi nhân " , ', '" mã đáo lai bách quan thất sắc đế diệc đại tư viên thiệu sậu mã xuất gian hà nhân kỳ thành ảnh lý nhất tướng phi xuất lệ thanh vấn thiên tử hà vãng đế chiến rất bất năng ngôn trần lưu vương lắc " , ', '" mã hướng tiền rất viết lai giả hà nhân trác viết tây lương lạt sử đổng xe dã trần lưu vương viết nhữ lai bảo cựu da nhữ lai kiếp vì da trác ưng viết được lai bảo giá trần lưu vương viết ký " , ', '" lai bảo giá thiên tử tại thử hà bất hạ mã trác đại kinh hoảng mang hạ mã bái ở đạo tả trần lưu vương dĩ ngôn phủ uỷ cái trác từ xưa chí chung tịnh vô thất ngữ trác ám kỳ chi dĩ " , ', '" hoài phế lập chi ý thị viết tuyển cung kiến hà thái hậu câu các thống khốc kiểm điểm cung trung bất kiến liễu truyền quốc ngọc nhĩ đổng trác đồn binh thành ngoại mỗi viết đái thiết giáp mã quân nhập thành hoành " , ', '" hành nhai thị bách tính hoàng hoàng bất an trác xuất nhập cung đình lược vô kỵ đạn hậu quân hiệu uý bào tín lai kiến viên thiệu ngôn đổng trác tất hữu dị tâm khả tốc trừ chi thiệu viết triều đình tân " , ', '" định vị khả khinh động bào tín kiến vương doãn diệc ngôn kỳ sự doãn viết thả dung thương nghị tin từ dẫn bản bộ quân binh đầu thái sơn khứ liễu hoạ xa chiêu dụ hà tiến huynh đệ bộ hạ chi binh " , ', '" tận quy chưởng ốc tư vị lý nguỵ viết ngô dục phế đế lập trần lưu vương hà như lý nho viết kim triều đình vô chủ bất tựu thử thời hành đình trì tắc hữu biến hãy lai viết ở ôn minh quốc " , ', '" trung triệu tập bá quan luận dĩ phế lập hữu bất tòng giả trảm chi tắc uy quyền chi hành chính tại kim nhật trác hỉ thứ nhật đại bày diên hội biến thỉnh công khanh công khanh giai cụ đổng trác thuỳ dám " ', '] ', '] ']

    # Thực thi hàm
    cleaned_data = clean_text_list(raw_data)

    # In kết quả
    print(cleaned_data)
