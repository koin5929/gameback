import os, httpx, discord
from discord import app_commands
from discord.ext import commands

BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN", "")
API_BASE  = os.getenv("API_BASE", "http://localhost:8000")
SECRET    = os.getenv("SHARED_SECRET", "CHANGE_ME_32CHARS")
GUILD_ID  = os.getenv("GUILD_ID")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

async def validate_name(name: str) -> dict:
    url = f"{API_BASE}/api/validate-name"
    async with httpx.AsyncClient(timeout=10.0) as client:
        r = await client.get(url, params={"name": name})
        r.raise_for_status(); return r.json()

async def register(discord_id: str, nickname: str, mc_name: str):
    url = f"{API_BASE}/api/register"
    headers = {"X-Prelaunch-Secret": SECRET}
    payload = {"discord_id": discord_id, "nickname": nickname, "mc_name": mc_name}
    async with httpx.AsyncClient(timeout=10.0) as client:
        r = await client.post(url, json=payload, headers=headers)
        return r

class ReservationModal(discord.ui.Modal, title="사전예약 · 마인크래프트 닉네임 확인"):
    mc_name = discord.ui.TextInput(label="마인크래프트 닉네임",
                                   placeholder="대소문자 포함 3~16자",
                                   min_length=3, max_length=16, required=True)
    def __init__(self, user: discord.User):
        super().__init__(timeout=180); self.user = user
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        name = str(self.mc_name.value).strip()
        try: v = await validate_name(name)
        except Exception: return await interaction.followup.send("⚠️ 검증 서버 연결 실패.", ephemeral=True)
        if not v.get("ok"): return await interaction.followup.send("❌ 존재하지 않는 닉네임입니다.", ephemeral=True)
        try:
            r = await register(str(self.user.id), interaction.user.display_name, name)
            if r.status_code in (200,201):
                return await interaction.followup.send(
                    f"✅ 사전예약 완료!\n- 디스코드: {interaction.user.mention}\n- 마크 닉네임: **{v.get('name', name)}**",
                    ephemeral=True)
            elif r.status_code == 409:
                return await interaction.followup.send("✅ 이미 사전예약된 계정입니다. (계정당 1회)", ephemeral=True)
            elif r.status_code == 422:
                return await interaction.followup.send("❌ 유효하지 않은 닉네임입니다.", ephemeral=True)
            else:
                return await interaction.followup.send(f"⚠️ 처리 실패({r.status_code}). 잠시 후 재시도.", ephemeral=True)
        except Exception:
            return await interaction.followup.send("⚠️ 서버 연결 실패. 잠시 후 재시도.", ephemeral=True)

class ReservationView(discord.ui.View):
    def __init__(self): super().__init__(timeout=None)
    @discord.ui.button(label="사전 예약하기", style=discord.ButtonStyle.primary, custom_id="prelaunch:reserve:open")
    async def open_modal(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(ReservationModal(interaction.user))

@bot.tree.command(name="사전예약패널", description="사전 예약 버튼 패널을 이 채널에 게시합니다.")
@app_commands.checks.has_permissions(manage_guild=True)
async def prelaunch_panel(interaction: discord.Interaction):
    embed = discord.Embed(
        title="LOSS ONLINE · 사전예약",
        description=(
            "아래 **[사전 예약하기]** 버튼을 누르고 **마인크래프트 닉네임**을 입력하세요.\n"
            "• 닉네임 실존 여부 확인 후 사전예약이 완료됩니다.\n"
            "• 디스코드 계정당 **1회만** 가능합니다.\n"
            "• 홈페이지 ‘사전예약 명단’에 자동 반영됩니다."
        ), color=0x2b6cb0
    )
    await interaction.response.send_message("패널을 게시했습니다.", ephemeral=True)
    await interaction.channel.send(embed=embed, view=ReservationView())

async def run_bot():
    if not BOT_TOKEN:
        print("DISCORD_BOT_TOKEN missing; bot will not start")
        return
    @bot.event
    async def on_ready():
        bot.add_view(ReservationView())
        try:
            if GUILD_ID: await bot.tree.sync(guild=discord.Object(id=int(GUILD_ID)))
            else: await bot.tree.sync()
        except Exception as e: print("Slash sync failed:", e)
        print(f"Discord bot logged in as {bot.user}")
    await bot.start(BOT_TOKEN)
