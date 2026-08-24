CREATE DATABASE research_db;
USE research_db;

INSERT INTO users(email, password_hash, full_name, role, is_active, created_at)
VALUES
	('ahiru@gmail.com', '$2b$12$teiOTRUMqOcAiclWR3m1fe2MnkTLhx2eDnQPYEnjxvlLbghKJ07Gi', 'Dansuraito Ahiru', 'ADMIN', 1, NOW()),
	('thai36@gmail.com', '$2b$12$i3NBLBaO9fjJMQgd2SRRDus88p9KKgV7nMmQ4N2nbzBuRcGuyxWxe', 'Pẹm Thái', 'USER', 1, NOW()),
	('cvnhatthong@gmail.com', '$2b$12$i3NBLBaO9fjJMQgd2SRRDus88p9KKgV7nMmQ4N2nbzBuRcGuyxWxe', 'Diêm Nhất Thống', 'USER', 1, NOW()),
	('cadin@gmail.com', '$2b$12$i3NBLBaO9fjJMQgd2SRRDus88p9KKgV7nMmQ4N2nbzBuRcGuyxWxe', 'Ca Din', 'USER', 1, NOW()),
	('truncongsuy@gmail.com', '$2b$12$i3NBLBaO9fjJMQgd2SRRDus88p9KKgV7nMmQ4N2nbzBuRcGuyxWxe', 'Trưn Cong Suy', 'USER', 0, NOW());
    
INSERT INTO research_projects(name, description, owner_id, created_at)
VALUES
	('Hệ thống quản lý nghiên cứu khoa học', 'Xây dựng hệ thống quản lý đề tài và nhiệm vụ nghiên cứu', 2, NOW()),
	('Ứng dụng AI trong giáo dục', 'Nghiên cứu ứng dụng AI hỗ trợ quá trình học tập', 3, NOW()),
	('Phân tích dữ liệu sinh viên', 'Phân tích dữ liệu để đánh giá kết quả học tập', 4, NOW());	
    
INSERT INTO research_members(project_id, user_id, role, joined_at)
VALUES
	(1, 2, 'OWNER', NOW()),
	(1, 3, 'MEMBER', NOW()),
	(1, 4, 'MEMBER', NOW()),
	(2, 3, 'OWNER', NOW()),
	(2, 2, 'MEMBER', NOW()),
	(2, 5, 'MEMBER', NOW()),
	(3, 4, 'OWNER', NOW()),
	(3, 2, 'MEMBER', NOW());
    
INSERT INTO research_tasks(project_id, title, description, assignee_id, status, priority, due_date, created_at)
VALUES
(1, 'Thiết kế database', 'Thiết kế cơ sở dữ liệu cho hệ thống', 3, 'DONE', 'HIGH', '2026-09-01 23:59:59', NOW()),
(1, 'Xây dựng API', 'Xây dựng REST API bằng FastAPI', 2, 'IN_PROGRESS', 'HIGH', '2026-09-10 23:59:59', NOW()),
(1, 'Viết tài liệu', 'Viết tài liệu hướng dẫn sử dụng', 4, 'TODO', 'LOW', '2026-09-15 23:59:59', NOW()),
(2, 'Thu thập dữ liệu', 'Thu thập dữ liệu phục vụ nghiên cứu', 5, 'IN_PROGRESS', 'MEDIUM', '2026-09-05 23:59:59', NOW()),
(2, 'Xây dựng mô hình AI', 'Huấn luyện mô hình AI', 3, 'TODO', 'HIGH', '2026-09-20 23:59:59', NOW()),
(2, 'Đánh giá kết quả', 'Đánh giá độ chính xác của membersmô hình', 2, 'TODO', 'MEDIUM', '2026-09-25 23:59:59', NOW()),
(3, 'Thu thập dữ liệu sinh viên', 'Chuẩn bị dataset', 4, 'DONE', 'HIGH', '2026-08-25 23:59:59', NOW()),
(3, 'Phân tích dữ liệu', 'Phân tích kết quả học tập', 2, 'IN_PROGRESS', 'HIGH', '2026-09-12 23:59:59', NOW());