# Yêu cầu đồ án Nhập môn Học máy

Nguồn: tab **Thông tin đồ án** trong [Google Docs của nhóm](https://docs.google.com/document/d/1BXscOQX-TQZYzKy0HOXoMgYcpc5V_lgIFqZvYFJ9c1g/edit?tab=t.0), lấy ngày 31/10/2026 (Asia/Saigon), cùng [phần bổ sung slide](requirements/nguon-bo-sung-slide.txt) người dùng cung cấp.

> Đây là bản trình bày lại ghi chú do người dùng cung cấp, không phải xác nhận độc lập toàn bộ quy định môn học. Khi có thay đổi hoặc khác biệt, kiểm tra Moodle và hướng dẫn giảng viên. Giữ bản chụp nguyên nội dung tại [nguồn Google Docs](requirements/nguon-google-docs.txt).

**Hạn nộp slide:** 23:59, Thứ Bảy 21/11/2026. **Tên file:** `ID.pptx`. **Quy cách:** 20-40 slide, tính cả phụ lục; dưới 20 MB; mọi slide có speaker notes tối đa 500 từ. Nộp link repo công khai thành mục riêng trên Moodle.

## 1. Tổng thể đồ án
- Mỗi nhóm chọn một paper ML để nghiên cứu xuyên suốt học kỳ
- Công việc gồm: đọc hiểu → tự triển khai → tái tạo thực nghiệm → phê bình lý thuyết → thực nghiệm kiểm chứng
- Có ba mốc nộp chính: đăng ký paper → slide → poster
- Cuối kỳ thi vấn đáp tại poster symposium
- Mỗi thành viên phải hiểu và giải thích được toàn bộ sản phẩm, không chỉ phần mình làm
## 2. Chủ đề và điều kiện chọn paper
- Chủ đề: never-ending learning
- Các hướng được nêu:
- Continual learning: task adaptation, task generalizability, grateful forgetting, task-free continual learning…
- Online learning: data streams, regret minimization, memory-based systems, concept drift…
- Lifelong learning: curriculum learning, persistent learning, self-reflection systems…
- Paper phải có đóng góp ML rõ ràng, phù hợp chủ đề
- Khuyến nghị dùng phương pháp dựa trên mô hình đã học ở lớp lý thuyết:

- Introduction
- DecisionTrees
- KNN
- OVerfitting
- - Linear Regression + SVM
- Linear Regression
- Linear Classification Perceptron
- Logistic Regression
- Learning Theory
- SVMs
- - Classifications
- Ensemble Methods
- Probability
- Bayes
- Text
- Neural Networks
- - Learning & Features
- Deeplearning
- Unsupervising
- Reinforcement
- Demensionality
- Features
- Networkleaning
- Large Scale
- Phải kiểm tra tài nguyên và khả năng tái tạo thực nghiệm trước khi chốt paper
## 3. Điều kiện tuổi bài
- Có tháng xuất bản: tối đa 60 tháng tính đến tháng đăng ký, đúng 60 tháng vẫn được
- Không có tháng: chỉ nhận bài trong năm đăng ký và hai năm trước
- Nếu đăng ký năm 2026 thì bài không có tháng phải thuộc 2024-2026
## 4. Điều kiện chất lượng paper
Đạt một trong hai đường:

| Đường xét | Điều kiện |
| --- | --- |
| Nơi xuất bản | Hội nghị CORE A/A* hoặc tạp chí SCIE Q1 |
| Citation | Nơi xuất bản không đạt hoặc chỉ là preprint thì xét Google Scholar, ngưỡng theo tuổi tháng × 2 citations |

- Dùng phiên bản xếp hạng thầy chỉ định: CORE2026 hoặc SCIE 2025/2024
- Không có tháng thì quy đổi tuổi năm thành tháng bằng cách nhân 12
- Đạt citation vẫn phải đáp ứng điều kiện tuổi bài, chủ đề và khả năng thực nghiệm
## 5. Đăng ký
- Đọc Google Form và Topics sheet
- Cử đại diện đăng ký theo quy định trên Moodle
- Paper được chấp nhận sẽ gắn với nhóm suốt học kỳ
- Deadline theo Moodle
## 6. Phạm vi tái tạo thực nghiệm - nhóm được chọn một trong hai

| Phạm vi | Yêu cầu |
| --- | --- |
| Đầy đủ | Tất cả thí nghiệm chính của paper, trên cùng dataset hoặc dataset tương đương |
| Cốt lõi | Ít nhất hai thí nghiệm quan trọng nhất, có phép so sánh chính của paper, đồng thời làm phân tích bổ sung do nhóm tự thiết kế để bù phần bỏ qua |

- Nêu rõ phạm vi đã chọn và lý do trong slide
- Chọn cốt lõi không có nghĩa chỉ chạy hai thí nghiệm rồi dừng
- Phân tích bổ sung có thể là quét độ nhạy tham số/cấu hình
- Mục tiêu không phải ép kết quả khớp tuyệt đối, mà là đo sai lệch và giải thích được vì sao
## 7. Quy định triển khai
- Tự implement từ mô tả trong paper
- Code tác giả được phép đọc, chạy, đối chiếu
- Không copy code gốc vào code nhóm, không nộp code gốc như sản phẩm của mình
- Nếu paper có code, phải chạy và so sánh với bản nhóm triển khai, xác định chỗ hai quy trình khác nhau
- Dùng Python ≥ 3.9
- Bộ công cụ tiêu chuẩn: numpy, scipy, scikit-learn
- Khi cần deep learning: torch, tensorflow hoặc jax
- Công cụ khác thường phải được giải thích trong README
- Các hàm quan trọng phải có docstring: mục đích, tham số, giá trị trả về
- README phải hướng dẫn thiết lập và chạy toàn bộ
## 8. Dữ liệu, nền tảng và khả năng tái lập
- Nhóm tự chọn nền tảng: máy cá nhân, cloud, hosted notebook…
- Không bắt buộc một nền tảng cụ thể, không bắt buộc nhân bản notebook
- Các lần chạy phải thật, đã hoàn thành và được ghi chép đầy đủ
- Cố định và ghi lại random seed
- Phải đảm bảo người khác có thể tái lập lần chạy
- Ưu tiên dataset công khai sẵn trên Hugging Face hoặc Kaggle hơn bản sao mới tải lên
- Code chuẩn bị dữ liệu phải nằm cùng code thực nghiệm để chạy lại được toàn bộ quy trình
## 9. Repository và W&B
- Duy trì repository công khai từ tuần đầu
- Chứa code, notebook, ghi chú, tài liệu và code chuẩn bị dữ liệu
- Commit sớm, thường xuyên; giữ lịch sử tiến độ và nhánh làm việc
- Nội dung slide/poster phải truy được về repo
- Mọi thí nghiệm phải được log vào W&B project công khai
- Log cấu hình, metrics và biểu đồ
- Mỗi số liệu của nhóm trên slide/poster phải dẫn đến W&B run tương ứng
- Hai phần tái tạo và kiểm chứng dùng cùng W&B project, nhưng gắn tag riêng để phân biệt
README phải có bảng:

| Thí nghiệm | Notebook/script tạo kết quả | Link W&B run | Kết quả tóm tắt |
| --- | --- | --- | --- |

## 10. Kết quả tái tạo bắt buộc có
- Với từng thí nghiệm trong phạm vi đã chọn:
- Kết quả paper công bố
- Kết quả nhóm đo được
- Độ lệch tương đối
- Giải thích mọi sai lệch đáng chú ý, xem xét:
- Cấu hình paper mô tả thiếu
- Khác biệt thư viện và phiên bản
- Khởi tạo ngẫu nhiên
- Phần cứng
- Nếu có code tác giả: so sánh đầu ra và chỉ ra khác biệt trong quy trình
- Đưa bảng so sánh và phân tích sai lệch vào phần kết quả của slide
- Code, notebook và lịch sử làm việc nằm trong repo
## 11. Phần slide – 45%
Hạn nộp: Thứ Bảy, 21/11/2026, 23:59.
Báo cáo giai đoạn 2 gộp đọc hiểu paper (Reading the Paper) + tái tạo thực nghiệm (Experimental Reproduction), gồm kết quả milestone 2 và bài lab tương ứng, trong một bộ slide.
### 11.1. Mục tiêu và cách đọc paper
- Nhóm phải hiểu và giải thích được khi không mở PDF: paper giải quyết bài toán gì, lấp khoảng trống nào, điểm mới thực sự là gì, phương pháp hoạt động ra sao và tác giả đánh giá thế nào.
- Diễn đạt bằng lời của nhóm, đủ rõ cho người chấm chưa đọc paper; chép nguyên câu hoặc chỉ kể lại paper không đáp ứng yêu cầu.
- Thứ tự đọc khuyến nghị: abstract → introduction → conclusion → background/related work → experiments → method.
- Sau lượt đọc nhanh, phải nói rõ paper hứa hẹn điều gì và đạt được gì; nếu chưa làm được thì đọc lại và cân nhắc lại lựa chọn paper.
### 11.2. Nội dung đọc hiểu bắt buộc
Bối cảnh và động lực
- Nêu bài toán bằng lời dễ hiểu, kèm một ví dụ thực tế do nhóm tự nghĩ để giải thích vì sao bài toán quan trọng.
- Phân tích ít nhất 2 phương pháp tiền nhiệm mà paper kế thừa: ý tưởng chính → hạn chế còn lại → hệ quả thực tế của hạn chế đó.
Đóng góp và tính mới
- Liệt kê các đóng góp đúng theo cách paper tuyên bố, sau đó phân loại thành đóng góp lý thuyết, kỹ thuật và thực nghiệm.
- Với từng đóng góp, đối chiếu các phương pháp tiền nhiệm để chỉ rõ điều gì trước đây chưa làm được hoặc chưa được thử.
Phương pháp – trình bày đủ 5 lớp
- Ký hiệu và bài toán hình thức: diễn đạt lại toàn bộ ký hiệu bằng một hệ ký hiệu nhất quán của nhóm; phát biểu bài toán dưới dạng hình thức khi paper có trình bày hình thức.
- Pipeline tổng thể: tự vẽ sơ đồ từ đầu vào đến đầu ra, giải thích dữ liệu đi qua từng bước.
- Từng thành phần: giải thích nó làm gì, vì sao cần và hoạt động chính xác thế nào. Công thức quan trọng phải giải thích mọi biến; ý nghĩa và lập luận đi kèm nằm trong speaker notes.
- Tính chất lý thuyết: diễn đạt lại mọi bổ đề, định lý hoặc phác thảo chứng minh mà paper nêu; giải thích trực quan điều được bảo đảm, điều kiện và giới hạn. Không yêu cầu chép lại đầy đủ chứng minh.
- Độ phức tạp: phân tích thời gian và bộ nhớ, đối chiếu với các phương pháp tiền nhiệm đã nêu.
### 11.3. Thiết lập và kết quả tái tạo
- Trực quan hóa cách đánh giá: datasets, metrics và protocol; nêu phạm vi tái tạo đã chọn cùng lý do.
- Kết thúc câu chuyện bằng kết quả tái tạo của nhóm, đặt cạnh kết quả paper.
- Có bảng đối chiếu cho từng thí nghiệm: kết quả paper → kết quả nhóm → độ lệch tương đối → giải thích sai lệch đáng chú ý.
- Mỗi số liệu của nhóm phải dẫn tới W&B run tương ứng; nếu có code tác giả, so sánh đầu ra và chỉ rõ khác biệt trong quy trình theo yêu cầu phần tái tạo.
### 11.4. Quy cách bộ slide
- Một file PPTX, từ 20 đến 40 slide, tính cả nội dung chính và phụ lục.
- Slide là sản phẩm trực quan: thể hiện đóng góp, tính mới, khoảng trống, phương pháp và cách đánh giá bằng hình, sơ đồ, bảng; tránh nhồi đoạn văn hoặc mã nguồn thô.
- Mọi slide đều phải có speaker notes, tối đa 500 từ/slide. Notes chứa phân tích, lập luận và phần giải thích không thể đặt hết trên hình.
- Không có thuyết trình miệng ở mốc slide. Người chấm đọc slide cùng notes đã nộp và đối chiếu các tuyên bố với paper; slide + notes là toàn bộ sản phẩm được đánh giá.
- Trích dẫn IEEE có đánh số ở cuối từng slide sử dụng nguồn. Không làm slide tài liệu tham khảo riêng; tuyên bố và nguồn phải nằm trên cùng slide.
- Tất cả hình phải do nhóm tự vẽ hoặc tái tạo. Không dán hình từ paper; việc đó được tính là sao chép theo quy định liêm chính.
- Slide thiếu speaker notes được tính là chưa hoàn chỉnh; slide đổ mã nguồn thô không đạt yêu cầu trực quan.
### 11.5. Nộp bài qua Moodle
- Tên file: ID.pptx, trong đó ID là số nguyên ID nhóm đã đăng ký trên sheet lập nhóm.
- Chỉ một file PPTX dưới 20 MB, đã bao gồm speaker notes; tải file slide lên riêng.
- Nộp link repository công khai có lịch sử theo dõi thành một mục riêng trên Moodle.
- File vượt giới hạn dung lượng hoặc thiếu link repository thì checkpoint được xem là chưa nộp cho đến khi sửa xong.

## 12. Phê bình lý thuyết phải xem những gì

| Khía cạnh | Câu hỏi cần xét |
| --- | --- |
| Giả định ngầm | Giả định về phân phối, tính độc lập/cấu trúc, dữ liệu và nhãn, độ mượt tối ưu hóa, mô hình tính toán có thực tế không? Khi vi phạm thì sao? |
| Tính đúng của tuyên bố | Bổ đề, định lý, tính chất có được chứng minh đúng không? Có điều kiện quan trọng bị giấu hoặc nói quá nhẹ không? |
| Bằng chứng hỗ trợ | Thực nghiệm thực sự hỗ trợ đến đâu? Có tuyên bố nào vượt quá bằng chứng không? |
| Cách đặt bài toán và mục tiêu | Hàm mục tiêu có phản ánh đúng điều paper muốn đạt không? Có shortcut, tác dụng phụ của regularization hoặc nghiệm suy biến không? |
| Độ phức tạp | Các giả định khi tính độ phức tạp có hợp lý không? Lợi thế có tồn tại ở quy mô thực nghiệm thực tế không? |
| Tính tổng quát | Phương pháp áp dụng được ngoài phạm vi đã đánh giá đến đâu? Lý thuyết nào hỗ trợ điều đó? |

Phần này tập trung vào lập luận lý thuyết; bằng chứng chạy thử được triển khai ở phần thực nghiệm kiểm chứng
## 13. Số lượng nội dung phê bình tối thiểu
- Ít nhất 3 điểm mạnh, mỗi điểm có lập luận và bằng chứng từ paper hoặc kết quả tái tạo
- Ít nhất 2 hạn chế lý thuyết, mỗi hạn chế được lập luận rõ và đủ cụ thể để thiết kế thí nghiệm kiểm tra
- Ít nhất 2 hướng nghiên cứu tương lai, xuất phát từ phát hiện trong phần phê bình
- Khen có bằng chứng cũng có giá trị chấm điểm như phê bình có bằng chứng
- Không bắt buộc phải sửa được phương pháp; trọng tâm là nhận diện và kiểm chứng hạn chế
## 14. Thực nghiệm kiểm chứng hạn chế
Chọn thí nghiệm phù hợp với hạn chế đã nêu, các dạng gợi ý gồm:

| Dạng | Cách làm |
| --- | --- |
| Vi phạm giả định | Thay đổi dữ liệu để phá giả định, đo mức suy giảm |
| Đối kháng/OOD | Đẩy phương pháp ra ngoài điều kiện đã đánh giá |
| Ablation | Bỏ hoặc làm yếu thành phần, xem tính chất nào còn |
| Baseline thay thế | Thay thành phần bằng phương án đơn giản hơn để kiểm tra tính cần thiết |
| Scaling | Đo thời gian thực khi tăng kích thước, đối chiếu tuyên bố độ phức tạp |
| Sensitivity | Thay từng tham số/cấu hình để đo độ nhạy |

- Đây là các lựa chọn gợi ý, không phải yêu cầu phải làm đủ cả sáu dạng
- Thí nghiệm phải nối rõ với lập luận: hạn chế nào → kiểm tra thế nào → đo gì → kết quả cho thấy gì
- Áp dụng đầy đủ quy định implement, seed, tái lập và W&B như phần tái tạo
## 15. Poster - 50%
- File .pptx
- Đúng một slide
- Khổ A2 dọc
- Gộp phê bình lý thuyết + thực nghiệm kiểm chứng
- Đặt lập luận và bằng chứng cạnh nhau, liên kết theo từng vấn đề
- Số liệu phải có W&B run làm căn cứ
- Chọn các luận điểm quan trọng và bằng chứng rõ, không nhồi lại toàn bộ slide
- Nộp qua Moodle, kèm link repo cố định
- Tại symposium, trình bày trực tiếp từ poster và bảo vệ luận điểm trước giám khảo
## 16. Chấm điểm và liêm chính

| Hạng mục | Điểm |
| --- | --- |
| Đăng ký paper | Điều kiện bắt buộc |
| Slide: đọc hiểu + tái tạo | 45% |
| Poster: phê bình + kiểm chứng | 50% |
| Repo, W&B, định dạng sản phẩm | 5% |

- Không sao chép văn bản/hình ảnh paper, code gốc hoặc bài nhóm khác; vi phạm có thể làm mất hiệu lực đồ án
- AI được phép dùng, kể cả hỗ trợ viết và code
- Từng thành viên vẫn phải hiểu, kiểm tra và giải thích được toàn bộ sản phẩm
- Giảng viên có thể đánh giá bổ sung khi cần
