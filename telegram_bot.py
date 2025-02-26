import requests
from telegram import Bot, InputMediaPhoto
from datetime import datetime
import asyncio
from PIL import Image
from io import BytesIO

# Cấu hình token và chat_id
TELEGRAM_TOKEN = '7676338777:AAEfEqx8diFb8TtVfJKQNxWXE2xIrQ1S1Ug'  
GROUP_CHAT_ID = '@nohu_longcsn68'  

# Khởi tạo bot
bot = Bot(token=TELEGRAM_TOKEN)

# Hàm lấy dữ liệu từ API
def get_data_from_api(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()['data']
        else:
            print(f"Error: {response.status_code}")
            return []
    except Exception as e:
        print(f"Exception: {e}")
        return []

# Hàm tải và chỉnh sửa ảnh
def download_and_resize_image(image_url, size=(250, 250)):
    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            img = img.resize(size)
            img_byte_arr = BytesIO()
            img.save(img_byte_arr, format='PNG')
            img_byte_arr.seek(0)
            return img_byte_arr
        else:
            print(f"Failed to download image: {image_url}")
            return None
    except Exception as e:
        print(f"Error downloading and resizing image: {e}")
        return None

# Hàm tìm game có giá trị 'value' cao nhất
def get_game_with_highest_value(data):
    return max(data, key=lambda x: x['value']) if data else None

# Hàm lấy thông tin từ API
def prepare_message(api_url, manuf):
    data = get_data_from_api(api_url)
    game = get_game_with_highest_value(data)
    
    if game:
        return {
            "manuf": manuf,
            "name": game['name'],
            "value": game['value'],
            "min10": game['min10'],
            "logo": game['logo']
        }
    return None

# Hàm gửi tin nhắn + ảnh vào nhóm Telegram
async def send_combined_message():
    game_pg = prepare_message("https://www.helpslot.win/api/games?manuf=PG&requestFrom=H5", "PG")
    game_jili = prepare_message("https://www.helpslot.win/api/games?manuf=JILI&requestFrom=H5", "JILI")

    if game_pg and game_jili:
        today = datetime.now().strftime('%d/%m/%Y')

        # Nội dung tin nhắn
        message = (
            f"<b>          🌠🌠🌠  KHUNG GIỜ VÀNG  🌠🌠🌠</b>\n"
            f"<b>         🌟 Ngày:</b> <i>{today}</i>\n\n"

            f"🎰 <b>Game HOT - {game_pg['manuf']}</b> 🎰\n"
            f"🎮 <b>Tên game:</b> <i>{game_pg['name']}</i>\n"
            f"💰 <b>Tỷ lệ chiến thắng:</b> <i>{game_pg['value']}%</i>\n"
            f"🔥 <b>Tỷ lệ scatter, bonus:</b> <i>{game_pg['min10']}%</i>\n\n"

            f"🎰 <b>Game HOT - {game_jili['manuf']}</b> 🎰\n"
            f"🎮 <b>Tên game:</b> <i>{game_jili['name']}</i>\n"
            f"💰 <b>Tỷ lệ chiến thắng:</b> <i>{game_jili['value']}%</i>\n"
            f"🔥 <b>Tỷ lệ scatter, bonus:</b> <i>{game_jili['min10']}%</i>\n\n"

            f"🕒 <b>Khung giờ:</b> <i>Liên hệ <a href='https://t.me/longcsn68'>ADMIN</a></i>\n"
            f"🚀 CHÚC ANH EM TRONG THƯƠNG HỘI THẮNG LỚN! 🎉"
        )

        # Tải ảnh từ cả 2 game
        image_pg = download_and_resize_image(game_pg['logo'])
        image_jili = download_and_resize_image(game_jili['logo'])

        # Danh sách ảnh theo đúng định dạng InputMediaPhoto
        media_group = []
        if image_pg:
            media_group.append(InputMediaPhoto(media=image_pg))
        if image_jili:
            media_group.append(InputMediaPhoto(media=image_jili))

        try:
            # Nếu có ảnh, gửi ảnh trước
            if media_group:
                await bot.send_media_group(chat_id=GROUP_CHAT_ID, media=media_group)

            # Gửi tin nhắn sau ảnh
            await bot.send_message(chat_id=GROUP_CHAT_ID, text=message, parse_mode='HTML')

        except Exception as e:
            print(f"Error sending message: {e}")

# Chạy bot mỗi giờ
async def main():
    while True:
        await send_combined_message()
        await asyncio.sleep(7000)  # Gửi tin nhắn mỗi giờ

# Chạy bot
if __name__ == '__main__':
    asyncio.run(main())
