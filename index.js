console.log("a");
const Discord = require("discord.js");
const bot = new Discord.client();
const config = require("./config.json");

bot.login(config.token);

bot.on("ready", async () => {
    console.log("(nathbot) : lancé");
    bot.user.setActivity("Prêt a conquerir le monde");
});

bot.on("message", async message =>{
    if(message.author.bot) return;
    if(message.channel.type === "dm") return;
    
    let prefix=config.prefix;
    let messageArray=message.content.split(" ");
    let cmd=messageArray[0];
    let args=messageArray.slice(1);
    
    if(cmd === "${prefix}hello"){
        message.channel.send("Bonjour !");
    }
})
