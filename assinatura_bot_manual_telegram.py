import os
import json
import time
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# ===== CONFIGURAÇÕES =====
TOKEN = "8011766930:AAE_Hv7cx7CG3ijxeMydYt-a_b0TdeZysO4"
ADMIN_ID = 7190628476
GROUP_ID = -1003395458966
PHOTO_URL = "https://i.postimg.cc/2jwbdQ1Z/by-PKOFs-(Telegram)-(263)-2.jpg"
PIX_IMAGE_URL = "https://i.postimg.cc/GpqJSW2q/IMG-20251206-173813-644.jpg"

# Códigos PIX para cada plano
PIX_CODES = {
    "semanal": "00020126580014BR.GOV.BCB.PIX0136ee76cc9d-7542-478a-ba8b-31840b87595e520400005303986540514.905802BR5901N6001C62180514ASSINATURASVIP63049ABF",
    "mensal": "00020126580014BR.GOV.BCB.PIX0136ee76cc9d-7542-478a-ba8b-31840b87595e520400005303986540529.905802BR5901N6001C62180514ASSINATURASVIP6304E08A",
    "anual": "00020126580014BR.GOV.BCB.PIX0136ee76cc9d-7542-478a-ba8b-31840b87595e520400005303986540539.905802BR5901N6001C62180514ASSINATURASVIP63042D68",
    "vitalicio": "00020126580014BR.GOV.BCB.PIX0136ee76cc9d-7542-478a-ba8b-31840b87595e520400005303986540559.905802BR5901N6001C62180514ASSINATURASVIP6304A166"
}

# Arquivo para salvar dados dos usuários
USERS_FILE = "usuarios.json"

# ===== FUNÇÕES AUXILIARES =====
def carregar_usuarios():
    """Carrega dados dos usuários do arquivo"""
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def salvar_usuarios(usuarios):
    """Salva dados dos usuários no arquivo"""
    with open(USERS_FILE, 'w') as f:
        json.dump(usuarios, f, indent=2)

usuarios = carregar_usuarios()

# ===== COMANDO /START =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando inicial que mostra os planos"""
    user = update.effective_user
    
    if str(user.id) not in usuarios:
        usuarios[str(user.id)] = {
            "nome": user.first_name,
            "username": user.username,
            "plano": None,
            "expira_em": None,
            "ativo": False
        }
        salvar_usuarios(usuarios)
    
    mensagem = f"""
✧ 𝑶𝒍𝒂́, {user.first_name}… 𝒃𝒆𝒎-𝒗𝒊𝒏𝒅𝒐 𝒂𝒐 𝑽𝑰𝑷 𝒅𝒂 𝑻𝒓𝒂𝒄𝒚 ✧
 
𝑨𝒒𝒖𝒊 𝒆́ 𝒐 𝒍𝒖𝒈𝒂𝒓 𝒐𝒏𝒅𝒆 𝒆𝒖 𝒎𝒐𝒔𝒕𝒓𝒐 𝒎𝒆𝒖 𝒍𝒂𝒅𝒐 𝒎𝒂𝒊𝒔 𝒂𝒕𝒓𝒂𝒊𝒏𝒕𝒆, 𝒅𝒆𝒍𝒊𝒄𝒂𝒅𝒐 𝒆 𝒑𝒓𝒐𝒗𝒐𝒄𝒂𝒏𝒕𝒆… 𝒐 𝒕𝒊𝒑𝒐 𝒅𝒆 𝒄𝒐𝒏𝒕𝒆𝒖́𝒅𝒐 𝒒𝒖𝒆 𝒔𝒐́ 𝒑𝒐𝒖𝒄𝒐𝒔 𝒕𝒆̂𝒎 𝒂𝒄𝒆𝒔𝒔𝒐.
 
𝑨𝒒𝒖𝒊 𝒆́ 𝒊𝒏𝒕𝒊𝒎𝒐, 𝒆𝒙𝒄𝒍𝒖𝒔𝒊𝒗𝒐, 𝒆 𝒇𝒆𝒊𝒕𝒐 𝒑𝒂𝒓𝒂 𝒗𝒐𝒄𝒆̂ 𝒒𝒆 𝒈𝒐𝒔𝒕𝒂 𝒅𝒆 𝒖𝒎𝒂 𝒑𝒆𝒈𝒂𝒅𝒂 𝒎𝒂𝒊𝒔 𝒂𝒓𝒓𝒆𝒃𝒂𝒕𝒂𝒅𝒐𝒓𝒂.
 
𝑺𝒆𝒍𝒆𝒄𝒊𝒐𝒏𝒆 𝒐 𝒑𝒍𝒂𝒏𝒐, 𝒇𝒂𝒛𝒂 𝒐 𝒑𝒂𝒈𝒂𝒎𝒆𝒏𝒕𝒐 𝒆 𝒂𝒑𝒗𝒂𝒊… 𝒎𝒆𝒖 𝒂𝒄𝒆𝒔𝒔𝒐 𝒗𝒆𝒏𝒉𝒆 𝒆𝒎 𝒔𝒆𝒈𝒖𝒏𝒅𝒐𝒔.
 
✧ 𝑩𝒆𝒎-𝒗𝒊𝒏𝒅𝒐 𝒂𝒐 𝒎𝒆𝒖 𝒎𝒖𝒏𝒅𝒐 𝑽𝑰𝑷. ✧
"""
    
    keyboard = [
        [InlineKeyboardButton("𝑺𝒆𝒎𝒂𝒏𝒂𝒍 𝒑𝒐𝒓 𝑹$ 14,90", callback_data="plano_semanal")],
        [InlineKeyboardButton("𝑴𝒆𝒏𝒔𝒂𝒍 𝒑𝒐𝒓 𝑹$ 29,90", callback_data="plano_mensal")],
        [InlineKeyboardButton("𝑨𝒏𝒖𝒂𝒍 𝒑𝒐𝒓 𝑹$ 39,90", callback_data="plano_anual")],
        [InlineKeyboardButton("𝑽𝒊𝒕𝒂𝒍𝒊́𝒄𝒊𝒐 𝒑𝒐𝒓 𝑹$ 59,90", callback_data="plano_vitalicio")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=PHOTO_URL,
        caption=mensagem,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

# ===== CALLBACK DOS PLANOS =====
async def callback_planos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Processa a escolha do plano"""
    query = update.callback_query
    await query.answer()
    
    user_id = str(query.from_user.id)
    
    planos = {
        "plano_semanal": {
            "nome": "Semanal",
            "preco": "R$ 14,90",
            "dias": 7,
            "codigo_pix": PIX_CODES["semanal"]
        },
        "plano_mensal": {
            "nome": "Mensal",
            "preco": "R$ 29,90",
            "dias": 30,
            "codigo_pix": PIX_CODES["mensal"]
        },
        "plano_anual": {
            "nome": "Anual",
            "preco": "R$ 39,90",
            "dias": 365,
            "codigo_pix": PIX_CODES["anual"]
        },
        "plano_vitalicio": {
            "nome": "Vitalício",
            "preco": "R$ 59,90",
            "dias": 36500,
            "codigo_pix": PIX_CODES["vitalicio"]
        }
    }
    
    plano_escolhido = planos[query.data]
    usuarios[user_id]["plano_escolhido"] = plano_escolhido
    salvar_usuarios(usuarios)
    
    mensagem = f"""
✧ 𝑷𝒂𝒓𝒂𝒃𝒆́𝒏𝒔! 𝑽𝒐𝒄𝒆̂ 𝒆𝒔𝒄𝒐𝒍𝒉𝒆𝒖 𝒐 𝒑𝒍𝒂𝒏𝒐 {plano_escolhido['nome']} ✧

𝑷𝒓𝒐𝒏𝒕𝒊𝒏𝒉𝒐! 𝑷𝒂𝒓𝒂 𝒑𝒂𝒈𝒂𝒓, 𝒔𝒆𝒍𝒆𝒄𝒊𝒐𝒏𝒆 𝒂 𝒇𝒐𝒓𝒎𝒂 𝒅𝒆 𝒑𝒂𝒈𝒂𝒎𝒆𝒏𝒕𝒐 𝒂𝒃𝒂𝒊𝒙𝒐 𝒆 𝒔𝒊𝒈𝒂 𝒂𝒔 𝒊𝒏𝒔𝒕𝒓𝒖𝒄̧𝒐̃𝒆𝒔.
"""
    
    keyboard = [[InlineKeyboardButton("𝑷𝑰𝑿", callback_data="gerar_pix")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_caption(
        caption=mensagem,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

# ===== GERAR PIX =====
async def gerar_pix(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gera o PIX para pagamento"""
    query = update.callback_query
    await query.answer("𝑮𝒆𝒓𝒂𝒏𝒅𝒐 𝑷𝒂𝒈𝒂𝒎𝒆𝒏𝒕𝒐...")
    
    user_id = str(query.from_user.id)
    plano = usuarios[user_id].get("plano_escolhido", {})
    
    await query.edit_message_caption(
        caption="𝑮𝒆𝒓𝒂𝒏𝒅𝒐 𝑷𝒂𝒈𝒂𝒎𝒆𝒏𝒕𝒐...",
        parse_mode='Markdown'
    )
    
    await context.bot.send_chat_action(chat_id=query.message.chat_id, action="typing")
    time.sleep(2)
    
    mensagem = f"""
✧ 𝑷𝒂𝒈𝒂𝒎𝒆𝒏𝒕𝒐 𝑮𝒆𝒓𝒂𝒅𝒐 𝒄𝒐𝒎 𝑺𝒖𝒄𝒆𝒔𝒔𝒐 ✧

𝑽𝒂𝒍𝒐𝒓 𝒅𝒂 𝑻𝒓𝒂𝒏𝒔𝒂𝒄̧𝒂̃𝒐: {plano['preco']}
𝑷𝒓𝒂𝒛𝒐 𝑷𝒂𝒓𝒂 𝑷𝒂𝒈𝒂𝒎𝒆𝒏𝒕𝒐: 15 𝑴𝒊𝒏𝒖𝒕𝒐𝒔

𝑷𝒂𝒈𝒖𝒆 𝒆 𝒄𝒍𝒊𝒒𝒖𝒆 𝒏𝒐 𝒃𝒐𝒕𝒂̃𝒐 𝒂𝒃𝒂𝒊𝒙𝒐 𝒐𝒖 𝒆𝒏𝒗𝒊𝒆 𝒂𝒒𝒖𝒊 𝒏𝒐 𝒃𝒐𝒕 𝒐 𝒄𝒐𝒎𝒑𝒓𝒐𝒗𝒂𝒏𝒕𝒆 𝒅𝒆 𝒑𝒂𝒈𝒂𝒎𝒆𝒏𝒕𝒐 𝒑𝒂𝒓𝒂 𝒒𝒖𝒆 𝒔𝒆𝒖 𝒂𝒄𝒆𝒔𝒔𝒐 𝒔𝒆𝒋𝒂 𝒍𝒊𝒃𝒆𝒓𝒂𝒅𝒐.

𝑷𝒂𝒈𝒂𝒎𝒆𝒏𝒕𝒐 𝒗𝒊𝒂 𝑷𝑰𝑿
"""
    
    keyboard = [[InlineKeyboardButton("𝑷𝑰𝑿 𝑪𝒐𝒑𝒊𝒂 𝒆 𝑪𝒐𝒍𝒂", callback_data="mostrar_codigo_pix")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await context.bot.send_photo(
        chat_id=query.message.chat_id,
        photo=PIX_IMAGE_URL,
        caption=mensagem,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

# ===== MOSTRAR CÓDIGO PIX =====
async def mostrar_codigo_pix(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mostra o código PIX Copia e Cola"""
    query = update.callback_query
    await query.answer()
    
    user_id = str(query.from_user.id)
    plano = usuarios[user_id].get("plano_escolhido", {})
    codigo_pix = plano.get("codigo_pix", "CODIGO_NAO_CONFIGURADO")
    
    mensagem = f"""
✧ 𝑷𝒓𝒐𝒏𝒕𝒊𝒏𝒉𝒐 ✧

𝑷𝒂𝒓𝒂 𝒑𝒂𝒈𝒂𝒓, 𝒄𝒍𝒊𝒒𝒖𝒆 𝒏𝒂 𝒄𝒉𝒂𝒗𝒆 𝑷𝒊𝒙 𝒂𝒃𝒂𝒊𝒙𝒐 𝒑𝒂𝒓𝒂 𝒄𝒐𝒑𝒊𝒂𝒓 𝒆 𝒑𝒂𝒈𝒖𝒆 𝒏𝒐 𝒂𝒑𝒑 𝒅𝒐 𝒔𝒆𝒖 𝒃𝒂𝒏𝒄𝒐.

𝑼𝒕𝒊𝒍𝒊𝒛𝒆 𝒂 𝒐𝒑𝒄̧𝒂̃𝒐 𝑷𝑰𝑿 𝑪𝒐𝒑𝒊𝒂 𝒆 𝑪𝒐𝒍𝒂 𝒏𝒐 𝒔𝒆𝒖 𝒂𝒑𝒍𝒊𝒄𝒂𝒕𝒊𝒗𝒐 𝒃𝒂𝒏𝒄𝒂́𝒓𝒊𝒐 𝒐𝒖 𝒑𝒂𝒈𝒂𝒎𝒆𝒏𝒕𝒐 𝒗𝒊𝒂 𝑸𝑹 𝑪𝒐𝒅𝒆 𝒆𝒎 𝒂𝒍𝒈𝒖𝒏𝒔 𝒃𝒂𝒏𝒄𝒐𝒔.

`{codigo_pix}`

𝑰𝒎𝒑𝒐𝒓𝒕𝒂𝒏𝒕𝒆! 𝑨𝒑𝒐́𝒔 𝒐 𝒑𝒂𝒈𝒂𝒎𝒆𝒏𝒕𝒐, 𝒗𝒐𝒍𝒕𝒆 𝒏𝒆𝒔𝒕𝒂 𝒕𝒆𝒍𝒂 𝒑𝒂𝒓𝒂 𝒓𝒆𝒄𝒆𝒃𝒆𝒓 𝒐 𝒍𝒊𝒏𝒌 𝒅𝒆 𝒂𝒄𝒆𝒔𝒔𝒐.

𝑨𝒈𝒖𝒂𝒓𝒅𝒆 𝒂𝒍𝒈𝒖𝒏𝒔 𝒊𝒏𝒔𝒕𝒂𝒏𝒕𝒆𝒔 𝒑𝒂𝒓𝒂 𝒒𝒖𝒆 𝒏𝒐𝒔𝒔𝒐 𝒔𝒊𝒔𝒕𝒆𝒎𝒂 𝒓𝒆𝒄𝒆𝒃𝒂 𝒂 𝒄𝒐𝒏𝒇𝒊𝒓𝒎𝒂𝒄̧𝒂̃𝒐 𝒅𝒐 𝒔𝒆𝒖 𝒑𝒂𝒈𝒂𝒎𝒆𝒏𝒕𝒐 𝒑𝒆𝒍𝒐 𝒃𝒂𝒏𝒄𝒐.

𝑪𝒂𝒔𝒐 𝒏𝒂̃𝒐 𝒓𝒆𝒄𝒆𝒃𝒂 𝒐 𝒍𝒊𝒏𝒌 𝒂𝒖𝒕𝒐𝒎𝒂𝒕𝒊𝒄𝒂𝒎𝒆𝒏𝒕𝒆 𝒆𝒎 𝒄𝒆𝒓𝒄𝒂 𝒅𝒆 3 𝒎𝒊𝒏𝒖𝒕𝒐𝒔, 𝒄𝒍𝒊𝒒𝒖𝒆 𝒏𝒐 𝒃𝒐𝒕𝒂̃𝒐 𝒂𝒃𝒂𝒊𝒙𝒐.
"""
    
    keyboard = [[InlineKeyboardButton("𝑪𝒐𝒏𝒇𝒊𝒓𝒎𝒂𝒓 𝑷𝒂𝒈𝒂𝒎𝒆𝒏𝒕𝒐", callback_data="confirmar_pagamento")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_caption(
        caption=mensagem,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

# ===== CONFIRMAR PAGAMENTO =====
async def confirmar_pagamento(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Pede o comprovante ao usuário"""
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_caption(
        caption="✧ 𝑷𝒐𝒓 𝒇𝒂𝒗𝒐𝒓, 𝒆𝒏𝒗𝒊𝒆 𝒐 𝒄𝒐𝒎𝒑𝒓𝒐𝒗𝒂𝒏𝒕𝒆 𝒅𝒆 𝒑𝒂𝒈𝒂𝒎𝒆𝒏𝒕𝒐 𝒂𝒒𝒖𝒊 𝒏𝒐 𝒄𝒉𝒂𝒕 ✧\n\n𝑷𝒐𝒅𝒆 𝒔𝒆𝒓 𝒖𝒎𝒂 𝒇𝒐𝒕𝒐 𝒐𝒖 𝒑𝒓𝒊𝒏𝒕 𝒅𝒂 𝒕𝒆𝒍𝒂.",
        parse_mode='Markdown'
    )

# ===== RECEBER COMPROVANTE =====
async def receber_comprovante(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Recebe o comprovante do usuário"""
    user = update.effective_user
    user_id = str(user.id)
    
    if user_id not in usuarios or "plano_escolhido" not in usuarios[user_id]:
        await update.message.reply_text("𝑷𝒓𝒊𝒎𝒆𝒊𝒓𝒐 𝒆𝒔𝒄𝒐𝒍𝒉𝒂 𝒖𝒎 𝒑𝒍𝒂𝒏𝒐 𝒖𝒔𝒂𝒏𝒅𝒐 /start")
        return
    
    plano = usuarios[user_id]["plano_escolhido"]
    
    await update.message.reply_text(
        "✧ 𝑪𝒐𝒎𝒑𝒓𝒐𝒗𝒂𝒏𝒕𝒆 𝒓𝒆𝒄𝒆𝒃𝒊𝒅𝒐 ✧\n\n"
        "𝑺𝒆𝒖 𝒑𝒂𝒈𝒂𝒎𝒆𝒏𝒕𝒐 𝒆𝒔𝒕𝒂́ 𝒔𝒆𝒏𝒅𝒐 𝒂𝒏𝒂𝒍𝒊𝒔𝒂𝒅𝒐.\n"
        "𝑨𝒈𝒖𝒂𝒓𝒅𝒆 𝒂 𝒂𝒑𝒓𝒐𝒗𝒂𝒄̧𝒂̃𝒐 𝒅𝒐 𝒂𝒅𝒎𝒊𝒏𝒊𝒔𝒕𝒓𝒂𝒅𝒐𝒓.\n\n"
        "𝑽𝒐𝒄𝒆̂ 𝒔𝒆𝒓𝒂́ 𝒏𝒐𝒕𝒊𝒇𝒊𝒄𝒂𝒅𝒐 𝒂𝒔𝒔𝒊𝒎 𝒒𝒖𝒆 𝒇𝒐𝒓 𝒂𝒑𝒓𝒐𝒗𝒂𝒅𝒐.",
        parse_mode='Markdown'
    )
    
    keyboard = [
        [
            InlineKeyboardButton("𝑳𝒊𝒃𝒆𝒓𝒂𝒓 𝑨𝒄𝒆𝒔𝒔𝒐", callback_data=f"liberar_{user_id}"),
            InlineKeyboardButton("𝑵𝒂̃𝒐 𝑳𝒊𝒃𝒆𝒓𝒂𝒓", callback_data=f"negar_{user_id}")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    mensagem_admin = f"""
𝑵𝒐𝒗𝒐 𝑪𝒐𝒎𝒑𝒓𝒐𝒗𝒂𝒏𝒕𝒆 𝑹𝒆𝒄𝒆𝒃𝒊𝒅𝒐

𝑼𝒔𝒖𝒂́𝒓𝒊𝒐: {user.first_name}
𝑰𝑫: {user_id}
𝑼𝒔𝒆𝒓𝒏𝒂𝒎𝒆: @{user.username if user.username else 'sem username'}
𝑷𝒍𝒂𝒏𝒐: {plano['nome']}
𝑽𝒂𝒍𝒐𝒓: {plano['preco']}
"""
    
    if update.message.photo:
        await context.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=update.message.photo[-1].file_id,
            caption=mensagem_admin,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    elif update.message.document:
        await context.bot.send_document(
            chat_id=ADMIN_ID,
            document=update.message.document.file_id,
            caption=mensagem_admin,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

# ===== LIBERAR/NEGAR ACESSO =====
async def processar_acesso(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Libera ou nega o acesso do usuário"""
    query = update.callback_query
    await query.answer()
    
    action, user_id = query.data.split('_')
    
    if action == "liberar":
        plano = usuarios[user_id]["plano_escolhido"]
        dias = plano["dias"]
        data_expiracao = datetime.now() + timedelta(days=dias)
        
        usuarios[user_id]["plano"] = plano["nome"]
        usuarios[user_id]["expira_em"] = data_expiracao.strftime("%Y-%m-%d %H:%M:%S")
        usuarios[user_id]["ativo"] = True
        usuarios[user_id]["aviso_enviado"] = False
        salvar_usuarios(usuarios)
        
        try:
            await context.bot.unban_chat_member(
                chat_id=GROUP_ID,
                user_id=int(user_id),
                only_if_banned=True
            )
            
            invite_link = await context.bot.create_chat_invite_link(
                chat_id=GROUP_ID,
                member_limit=1,
                expire_date=int(time.time()) + 3600
            )
            
            await context.bot.send_message(
                chat_id=int(user_id),
                text=f"""
✧ 𝑷𝒂𝒈𝒂𝒎𝒆𝒏𝒕𝒐 𝑨𝒑𝒓𝒐𝒗𝒂𝒅𝒐 ✧

𝑺𝒆𝒖 𝒑𝒂𝒈𝒂𝒎𝒆𝒏𝒕𝒐 𝒇𝒐𝒊 𝒄𝒐𝒏𝒇𝒊𝒓𝒎𝒂𝒅𝒐!
𝑷𝒍𝒂𝒏𝒐: {plano['nome']}
𝑽𝒂́𝒍𝒊𝒅𝒐 𝒂𝒕𝒆́: {data_expiracao.strftime("%d/%m/%Y 𝒂̀𝒔 %H:%M")}

𝑳𝒊𝒏𝒌 𝒅𝒐 𝑮𝒓𝒖𝒑𝒐 𝑽𝑰𝑷:
{invite_link.invite_link}

𝑩𝒆𝒎-𝒗𝒊𝒏𝒅𝒐 𝒂𝒐 𝑽𝑰𝑷!
""",
                parse_mode='Markdown'
            )
            
            await query.edit_message_caption(
                caption=f"{query.message.caption}\n\n✧ 𝑨𝒄𝒆𝒔𝒔𝒐 𝑳𝒊𝒃𝒆𝒓𝒂𝒅𝒐 𝒄𝒐𝒎 𝑺𝒖𝒄𝒆𝒔𝒔𝒐 ✧",
                parse_mode='Markdown'
            )
            
        except Exception as e:
            await query.edit_message_caption(
                caption=f"{query.message.caption}\n\n𝑬𝒓𝒓𝒐: {str(e)}",
                parse_mode='Markdown'
            )
    
    elif action == "negar":
        await context.bot.send_message(
            chat_id=int(user_id),
            text="""
✧ 𝑷𝒂𝒈𝒂𝒎𝒆𝒏𝒕𝒐 𝑵𝒂̃𝒐 𝑨𝒑𝒓𝒐𝒗𝒂𝒅𝒐 ✧

𝑺𝒆𝒖 𝒄𝒐𝒎𝒑𝒓𝒐𝒗𝒂𝒏𝒕𝒆 𝒏𝒂̃𝒐 𝒇𝒐𝒊 𝒂𝒑𝒓𝒐𝒗𝒂𝒅𝒐.

𝑷𝒐𝒔𝒔𝒊́𝒗𝒆𝒊𝒔 𝒎𝒐𝒕𝒊𝒗𝒐𝒔:
𝑪𝒐𝒎𝒑𝒓𝒐𝒗𝒂𝒏𝒕𝒆 𝒊𝒍𝒆𝒈𝒊́𝒗𝒆𝒍
𝑽𝒂𝒍𝒐𝒓 𝒊𝒏𝒄𝒐𝒓𝒓𝒆𝒕𝒐
𝑫𝒂𝒅𝒐𝒔 𝒊𝒏𝒄𝒐𝒏𝒔𝒊𝒔𝒕𝒆𝒏𝒕𝒆𝒔

𝑬𝒏𝒕𝒓𝒆 𝒆𝒎 𝒄𝒐𝒏𝒕𝒂𝒕𝒐 𝒄𝒐𝒎 𝒐 𝒔𝒖𝒑𝒐𝒓𝒕𝒆 𝒑𝒂𝒓𝒂 𝒎𝒂𝒊𝒔 𝒊𝒏𝒇𝒐𝒓𝒎𝒂𝒄̧𝒐̃𝒆𝒔.
""",
            parse_mode='Markdown'
        )
        
        await query.edit_message_caption(
            caption=f"{query.message.caption}\n\n✧ 𝑨𝒄𝒆𝒔𝒔𝒐 𝑵𝒆𝒈𝒂𝒅𝒐 ✧",
            parse_mode='Markdown'
        )

# ===== COMANDO /ADM =====
async def adm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Menu do administrador"""
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("𝑽𝒐𝒄𝒆̂ 𝒏𝒂̃𝒐 𝒕𝒆𝒎 𝒑𝒆𝒓𝒎𝒊𝒔𝒔𝒂̃𝒐 𝒑𝒂𝒓𝒂 𝒖𝒔𝒂𝒓 𝒆𝒔𝒕𝒆 𝒄𝒐𝒎𝒂𝒏𝒅𝒐!")
        return
    
    total_usuarios = len(usuarios)
    usuarios_ativos = sum(1 for u in usuarios.values() if u.get("ativo"))
    usuarios_inativos = total_usuarios - usuarios_ativos
    
    hoje = datetime.now().date()
    vencem_hoje = 0
    for u in usuarios.values():
        if u.get("expira_em") and u.get("ativo"):
            expira = datetime.strptime(u["expira_em"], "%Y-%m-%d %H:%M:%S").date()
            if expira == hoje:
                vencem_hoje += 1
    
    mensagem = f"""
✧ 𝑷𝒂𝒊𝒏𝒆𝒍 𝒅𝒐 𝑨𝒅𝒎𝒊𝒏𝒊𝒔𝒕𝒓𝒂𝒅𝒐𝒓 ✧

𝑬𝒔𝒕𝒂𝒕𝒊́𝒔𝒕𝒊𝒄𝒂𝒔:

𝑻𝒐𝒕𝒂𝒍 𝒅𝒆 𝑼𝒔𝒖𝒂́𝒓𝒊𝒐𝒔: {total_usuarios}
𝑼𝒔𝒖𝒂́𝒓𝒊𝒐𝒔 𝑨𝒕𝒊𝒗𝒐𝒔: {usuarios_ativos}
𝑼𝒔𝒖𝒂́𝒓𝒊𝒐𝒔 𝑰𝒏𝒂𝒕𝒊𝒗𝒐𝒔: {usuarios_inativos}
𝑽𝒆𝒏𝒄𝒆𝒎 𝑯𝒐𝒋𝒆: {vencem_hoje}

𝑪𝒐𝒎𝒂𝒏𝒅𝒐𝒔 𝑫𝒊𝒔𝒑𝒐𝒏𝒊́𝒗𝒆𝒊𝒔:

/lista_ativos - 𝑽𝒆𝒓 𝒕𝒐𝒅𝒐𝒔 𝒐𝒔 𝒎𝒆𝒎𝒃𝒓𝒐𝒔 𝑽𝑰𝑷 𝒂𝒕𝒊𝒗𝒐𝒔
/lista_vencendo - 𝑽𝒆𝒓 𝒂𝒔𝒔𝒊𝒏𝒂𝒕𝒖𝒓𝒂𝒔 𝒒𝒖𝒆 𝒗𝒆𝒏𝒄𝒆𝒎 𝒆𝒎 𝒃𝒓𝒆𝒗𝒆
"""
    
    await update.message.reply_text(mensagem, parse_mode='Markdown')

# ===== LISTAR USUÁRIOS ATIVOS =====
async def lista_ativos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lista todos os usuários ativos"""
    if update.effective_user.id != ADMIN_ID:
        return
    
    ativos = [(uid, dados) for uid, dados in usuarios.items() if dados.get("ativo")]
    
    if not ativos:
        await update.message.reply_text("𝑵𝒆𝒏𝒉𝒖𝒎 𝒖𝒔𝒖𝒂́𝒓𝒊𝒐 𝒂𝒕𝒊𝒗𝒐 𝒏𝒐 𝒎𝒐𝒎𝒆𝒏𝒕𝒐.")
        return
    
    mensagem = "✧ 𝑼𝒔𝒖𝒂́𝒓𝒊𝒐𝒔 𝑨𝒕𝒊𝒗𝒐𝒔 ✧\n\n"
    
    for uid, dados in ativos:
        expira = datetime.strptime(dados["expira_em"], "%Y-%m-%d %H:%M:%S")
        dias_restantes = (expira - datetime.now()).days
        
        mensagem += f"𝑼𝒔𝒖𝒂́𝒓𝒊𝒐: {dados['nome']}\n"
        mensagem += f"𝑰𝑫: `{uid}`\n"
        mensagem += f"𝑷𝒍𝒂𝒏𝒐: {dados['plano']}\n"
        mensagem += f"𝑬𝒙𝒑𝒊𝒓𝒂: {expira.strftime('%d/%m/%Y')}\n"
        mensagem += f"𝑫𝒊𝒂𝒔 𝒓𝒆𝒔𝒕𝒂𝒏𝒕𝒆𝒔: {dias_restantes}\n\n"
    
    await update.message.reply_text(mensagem, parse_mode='Markdown')

# ===== LISTAR VENCENDO =====
async def lista_vencendo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lista usuários que vão vencer em breve"""
    if update.effective_user.id != ADMIN_ID:
        return
    
    agora = datetime.now()
    vencendo = []
    
    for uid, dados in usuarios.items():
        if not dados.get("ativo") or dados.get("plano") == "Vitalício":
            continue
        
        expira = datetime.strptime(dados["expira_em"], "%Y-%m-%d %H:%M:%S")
        dias_restantes = (expira - agora).days
        
        if 0 <= dias_restantes <= 7:
            vencendo.append((uid, dados, dias_restantes, expira))
    
    if not vencendo:
        await update.message.reply_text("𝑵𝒆𝒏𝒉𝒖𝒎𝒂 𝒂𝒔𝒔𝒊𝒏𝒂𝒕𝒖𝒓𝒂 𝒗𝒆𝒏𝒄𝒆𝒏𝒅𝒐 𝒏𝒐𝒔 𝒑𝒓𝒐́𝒙𝒊𝒎𝒐𝒔 7 𝒅𝒊𝒂𝒔.")
        return
    
    vencendo.sort(key=lambda x: x[2])
    
    for uid, dados, dias, expira in vencendo:
        keyboard = [
            [
                InlineKeyboardButton("𝑴𝒂𝒏𝒕𝒆𝒓", callback_data=f"manter_{uid}"),
                InlineKeyboardButton("𝑩𝒂𝒏𝒊𝒓", callback_data=f"banir_{uid}")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        msg = f"""
✧ 𝑨𝒔𝒔𝒊𝒏𝒂𝒕𝒖𝒓𝒂 𝑽𝒆𝒏𝒄𝒆𝒏𝒅𝒐 ✧

𝑼𝒔𝒖𝒂́𝒓𝒊𝒐: {dados['nome']}
𝑰𝑫: `{uid}`
𝑷𝒍𝒂𝒏𝒐: {dados['plano']}
𝑬𝒙𝒑𝒊𝒓𝒂: {expira.strftime('%d/%m/%Y 𝒂̀𝒔 %H:%M')}
𝑫𝒊𝒂𝒔 𝒓𝒆𝒔𝒕𝒂𝒏𝒕𝒆𝒔: {dias}
"""
        
        await update.message.reply_text(msg, reply_markup=reply_markup, parse_mode='Markdown')

# ===== MANTER/BANIR USUÁRIO =====
async def processar_vencimento(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mantém ou bane o usuário"""
    query = update.callback_query
    await query.answer()
    
    action, user_id = query.data.split('_')
    
    if action == "manter":
        nova_expiracao = datetime.now() + timedelta(days=30)
        usuarios[user_id]["expira_em"] = nova_expiracao.strftime("%Y-%m-%d %H:%M:%S")
        usuarios[user_id]["aviso_enviado"] = False
        salvar_usuarios(usuarios)
        
        await context.bot.send_message(
            chat_id=int(user_id),
            text=f"""
✧ 𝑺𝒖𝒂 𝑨𝒔𝒔𝒊𝒏𝒂𝒕𝒖𝒓𝒂 𝒇𝒐𝒊 𝑹𝒆𝒏𝒐𝒗𝒂𝒅𝒂 ✧

𝑺𝒆𝒖 𝒂𝒄𝒆𝒔𝒔𝒐 𝒇𝒐𝒊 𝒎𝒂𝒏𝒕𝒊𝒅𝒐!
𝑵𝒐𝒗𝒂 𝒅𝒂𝒕𝒂 𝒅𝒆 𝒗𝒆𝒏𝒄𝒊𝒎𝒆𝒏𝒕𝒐: {nova_expiracao.strftime("%d/%m/%Y 𝒂̀𝒔 %H:%M")}

𝑪𝒐𝒏𝒕𝒊𝒏𝒖𝒆 𝒂𝒑𝒓𝒐𝒗𝒆𝒊𝒕𝒂𝒏𝒅𝒐 𝒐 𝒄𝒐𝒏𝒕𝒆𝒖́𝒅𝒐 𝑽𝑰𝑷!
""",
            parse_mode='Markdown'
        )
        
        await query.edit_message_text(
            f"{query.message.text}\n\n✧ 𝑼𝒔𝒖𝒂́𝒓𝒊𝒐 𝑴𝒂𝒏𝒕𝒊𝒅𝒐 - 𝑹𝒆𝒏𝒐𝒗𝒂𝒅𝒐 𝒂𝒕𝒆́ {nova_expiracao.strftime('%d/%m/%Y')} ✧",
            parse_mode='Markdown'
        )
    
    elif action == "banir":
        usuarios[user_id]["ativo"] = False
        salvar_usuarios(usuarios)
        
        try:
            await context.bot.ban_chat_member(
                chat_id=GROUP_ID,
                user_id=int(user_id)
            )
            
            await context.bot.send_message(
                chat_id=int(user_id),
                text="""
✧ 𝑺𝒖𝒂 𝑨𝒔𝒔𝒊𝒏𝒂𝒕𝒖𝒓𝒂 𝑬𝒙𝒑𝒊𝒓𝒐𝒖 ✧

𝑺𝒆𝒖 𝒂𝒄𝒆𝒔𝒔𝒐 𝒂𝒐 𝒈𝒓𝒖𝒑𝒐 𝑽𝑰𝑷 𝒇𝒐𝒊 𝒆𝒏𝒄𝒆𝒓𝒓𝒂𝒅𝒐.

𝑷𝒂𝒓𝒂 𝒓𝒆𝒏𝒐𝒗𝒂𝒓, 𝒖𝒔𝒆 /start 𝒆 𝒆𝒔𝒄𝒐𝒍𝒉𝒂 𝒖𝒎 𝒏𝒐𝒗𝒐 𝒑𝒍𝒂𝒏𝒐!
""",
                parse_mode='Markdown'
            )
            
            await query.edit_message_text(
                f"{query.message.text}\n\n✧ 𝑼𝒔𝒖𝒂́𝒓𝒊𝒐 𝑩𝒂𝒏𝒊𝒅𝒐 𝒅𝒐 𝑮𝒓𝒖𝒑𝒐 ✧",
                parse_mode='Markdown'
            )
        except Exception as e:
            await query.edit_message_text(
                f"{query.message.text}\n\n𝑬𝒓𝒓𝒐 𝒂𝒐 𝒃𝒂𝒏𝒊𝒓: {str(e)}",
                parse_mode='Markdown'
            )

# ===== COMANDO /MEUPLANO =====
async def meu_plano(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mostra informações do plano do usuário"""
    user_id = str(update.effective_user.id)
    
    if user_id not in usuarios or not usuarios[user_id].get("ativo"):
        await update.message.reply_text(
            "✧ 𝑽𝒐𝒄𝒆̂ 𝒏𝒂̃𝒐 𝒑𝒐𝒔𝒔𝒖𝒊 𝒖𝒎𝒂 𝒂𝒔𝒔𝒊𝒏𝒂𝒕𝒖𝒓𝒂 𝒂𝒕𝒊𝒗𝒂 ✧\n\n𝑼𝒔𝒆 /start 𝒑𝒂𝒓𝒂 𝒂𝒔𝒔𝒊𝒏𝒂𝒓!",
            parse_mode='Markdown'
        )
        return
    
    dados = usuarios[user_id]
    expira_em = datetime.strptime(dados["expira_em"], "%Y-%m-%d %H:%M:%S")
    dias_restantes = (expira_em - datetime.now()).days
    
    mensagem = f"""
✧ 𝑴𝒊𝒏𝒉𝒂 𝑨𝒔𝒔𝒊𝒏𝒂𝒕𝒖𝒓𝒂 ✧

𝑷𝒍𝒂𝒏𝒐: {dados['plano']}
𝑺𝒕𝒂𝒕𝒖𝒔: 𝑨𝒕𝒊𝒗𝒐
𝑬𝒙𝒑𝒊𝒓𝒂 𝒆𝒎: {expira_em.strftime("%d/%m/%Y 𝒂̀𝒔 %H:%M")}
𝑫𝒊𝒂𝒔 𝒓𝒆𝒔𝒕𝒂𝒏𝒕𝒆𝒔: {dias_restantes} 𝒅𝒊𝒂𝒔

𝑹𝒆𝒏𝒐𝒗𝒆 𝒔𝒖𝒂 𝒂𝒔𝒔𝒊𝒏𝒂𝒕𝒖𝒓𝒂 𝒂𝒏𝒕𝒆𝒔 𝒅𝒐 𝒗𝒆𝒏𝒄𝒊𝒎𝒆𝒏𝒕𝒐!
"""
    
    await update.message.reply_text(mensagem, parse_mode='Markdown')

# ===== MAIN =====
def main():
    """Função principal"""
    application = Application.builder().token(TOKEN).build()
    
    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("adm", adm))
    application.add_handler(CommandHandler("meuplano", meu_plano))
    application.add_handler(CommandHandler("lista_ativos", lista_ativos))
    application.add_handler(CommandHandler("lista_vencendo", lista_vencendo))
    
    application.add_handler(CallbackQueryHandler(callback_planos, pattern="^plano_"))
    application.add_handler(CallbackQueryHandler(gerar_pix, pattern="^gerar_pix$"))
    application.add_handler(CallbackQueryHandler(mostrar_codigo_pix, pattern="^mostrar_codigo_pix$"))
    application.add_handler(CallbackQueryHandler(confirmar_pagamento, pattern="^confirmar_pagamento$"))
    application.add_handler(CallbackQueryHandler(processar_acesso, pattern="^(liberar|negar)_"))
    application.add_handler(CallbackQueryHandler(processar_vencimento, pattern="^(manter|banir)_"))
    
    application.add_handler(MessageHandler(filters.PHOTO | filters.Document.ALL, receber_comprovante))
    
    print("✧ 𝑩𝒐𝒕 𝒊𝒏𝒊𝒄𝒊𝒂𝒅𝒐 𝒄𝒐𝒎 𝒔𝒖𝒄𝒆𝒔𝒔𝒐 ✧")
    print("✧ 𝑺𝒊𝒔𝒕𝒆𝒎𝒂 𝒅𝒆 𝒂𝒔𝒔𝒊𝒏𝒂𝒕𝒖𝒓𝒂𝒔 𝑽𝑰𝑷 𝒂𝒕𝒊𝒗𝒐 ✧")
    application.run_polling()

if __name__ == '__main__':
    main()
