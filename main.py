
import discord
from discord.ext import commands
from model import get_class

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Hi! I am a bot {bot.user}!')

@bot.command()
async def check(ctx):
    if ctx.message.attachments:
        for attachment in ctx.message.attachments:
            # Guardar la imagen adjunta
            await attachment.save(f"./{attachment.filename}")
            
            # Obtener la predicción
            try:
                class_name, confidence = get_class(
                    model_path="./keras_model.h5",
                    labels_path="./labels.txt",
                    image_path=f"./{attachment.filename}"
                )
                
                # Formatear la respuesta
                response = f"**Resultado:**\nClase: {class_name}\nConfianza: {confidence*100:.2f}%"
                await ctx.send(response)
                
            except Exception as e:
                await ctx.send(f"Ocurrió un error al procesar la imagen: {str(e)}")
    else:
        await ctx.send("Olvidaste subir una imagen :(")

bot.run("Inserta tu Token Aqui")
