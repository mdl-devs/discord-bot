@bot.command()
# cool down of 4 mins to counter spamming
@commands.cooldown(1, 240, commands.BucketType.user)
async def apply(ctx, *, args=None):
    applied_times = 0
    rate_limit_for_applications = 5
    time_to_wait_to_avoid_rate_limit = 60
    role = discord.utils.get(ctx.guild.roles, name="Applicant")
    await ctx.author.add_roles(role)
    await ctx.message.delete()
    await bot.wait_until_ready()
    applied_times += 1
    if args == None:
        message_content = "Please wait, we will be with you shortly!"

    else:
        message_content = "".join(args)

    with open("data.json") as f:
        data = json.load(f)
    ticket_number = int(data["ticket-counter"])
    ticket_number += 1
    category = discord.utils.get(
        ctx.guild.categories, name="| ðŽðŸðŸð¢ðœðž ð”ð¬ðž")
    ticket_channel = await ctx.guild.create_text_channel("application-{}".format(ticket_number), category=category)
    await ticket_channel.set_permissions(ctx.guild.get_role(ctx.guild.id), send_messages=False, read_messages=False)

    for role_id in data["valid-roles"]:
        role = ctx.guild.get_role(role_id)

        await ticket_channel.set_permissions(role, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)

    await ticket_channel.set_permissions(ctx.author, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)

    em = discord.Embed(title="New application from {}#{}".format(
        ctx.author.name, ctx.author.discriminator), description="{}".format(message_content), color=0x00a8ff)
    await ticket_channel.send(embed=em)
    em2 = discord.Embed(title="Welcome to Monndog Logistics Applications System",
                        description="To Become a driver at Moondog Logistics we ask u submit an application. To do this, reply to all the messages the bot will send you one at a time **It could take up to 1 - 2 days for a application to be viewed.**")
    await ticket_channel.send(embed=em2)
    pinged_msg_content = ""
    non_mentionable_roles = []

    if data["pinged-roles"] != []:

        for role_id in data["pinged-roles"]:
            role = ctx.guild.get_role(role_id)

            pinged_msg_content += role.mention
            pinged_msg_content += " "

            if role.mentionable:
                pass
            else:
                await role.edit(mentionable=True)
                non_mentionable_roles.append(role)

        await ticket_channel.send(pinged_msg_content)

        for role in non_mentionable_roles:
            await role.edit(mentionable=False)

    data["ticket-channel-ids"].append(ticket_channel.id)

    data["ticket-counter"] = int(ticket_number)
    with open("data.json", 'w') as f:
        json.dump(data, f)

    created_em = discord.Embed(title="Moondog Logistics Applications", description="Your application ticket has been created at {}".format(
        ticket_channel.mention), color=0x00a8ff)
    hook = Webhook(
        'https://discord.com/api/webhooks/827502772291239996/sH6UfgNFrVvKwAbdsFH2svKOGSEgHNhxwZ7V8UHyWikR3O4bFxID5QwSxNx3XKQcRq7c')
    userapplyed = discord.Embed(title="Moondog Logistics Applications",
                                description=f"{ctx.author.mention} Has applied.  Channel name:{ticket_channel.mention}")
    hook.send(embed=userapplyed)
    await ctx.send(embed=created_em)

    # checks to see if the user is a Diretor if they are then they will not be allowed to apply
    Diretor_role = discord.utils.get(ctx.guild.roles, id=837606126795227136)
    if Diretor_role in ctx.author.roles:
        await ticket_channel.delete()
        Member_has_too_high_role = discord.Embed(
            title="Moondog Logistics Applications | `apply` error", description=f"Hey {ctx.author.name}, you have the `director role` so you dont need to apply.", color=0xFF0000)
        global time_main2
        Member_has_too_high_role.set_footer(
            text=f"Moondog Logistics Applications | Apply Error Message â€¢ {time_main2}")
        await ctx.author.send(embed=Member_has_too_high_role)
    # sends a embed message logging to staff-logs stating that they tried to apply
        channel3 = discord.utils.get(ctx.guild.channels, id=837714802049679451)
        staff_log_messageing_1 = discord.Embed(
            ttitle="Moondog Logistics Applications | `apply` Logging Message", description=f"{ctx.author.name} Tried to apply to join the vtc tho there attempt was blocked because `They had the role name` **`Director`**", color=0xFF0000)
        staff_log_messageing_1.set_footer(
            text=f"Moondog Logistics Applications | Apply Logging Message â€¢ {time_main2}")
        await channel3.send(embed=staff_log_messageing_1)

    # checks to see if the user is already a driver and then they dont need to apply / cant apply. If they are abusing the system then it will flag to the staff team.
    Drivers_role = discord.utils.get(ctx.guild.roles, id=837666217413967882)
    if Drivers_role in ctx.author.roles:
        await ticket_channel.delete()
        Member_has_too_high_role_2 = discord.Embed(
            title="Moondog Logistics Applications | `apply` error", description=f"Hey {ctx.author.name}, you have the `drivers role` so you dont need to apply.", color=0xFF0000)
        Member_has_too_high_role_2.set_footer(
            text=f"Moondog Logistics Applications | Apply Error Message â€¢ {time_main2}")
        await ctx.author.send(embed=Member_has_too_high_role_2)
    # sends a embed message logging to staff-logs stating that they tried to apply
        channel2 = discord.utils.get(ctx.guild.channels, id=837714802049679451)
        staff_log_messageing_2 = discord.Embed(
            title="Moondog Logistics Applications | `apply` Logging Message", description=f"{ctx.author.name} Tried to apply to join the vtc tho there attempt was blocked because `They had the role name` **`Driver`**", color=0xFF0000)
        staff_log_messageing_1.set_footer(
            text=f"Moondog Logistics Applications | Apply Logging Message â€¢ {time_main2}")
        await channel2.send(embed=staff_log_messageing_2)

    # checks to see if the user is a member of lower staff, however they should have the above role anyway :)
    lower_staff_role = discord.utils.get(
        ctx.guild.roles, id=837606669830848523)
    if lower_staff_role in ctx.author.roles:
        await ticket_channel.delete()
        Member_has_too_high_role_3 = discord.Embed(
            title="Moondog Logistics Applications | `apply` error", description=f"Hey {ctx.author.name}, you have the `lower staff` role so you dont need to apply.", color=0xFF0000)
        Member_has_too_high_role_3.set_footer(
            text=f"Moondog Logistics Applications | Apply Error Message â€¢ {time_main2}")
        await ctx.author.send(embed=Member_has_too_high_role_3)
    # sends a embed message logging to staff-logs stating that they tried to apply
        channel1 = discord.utils.get(ctx.guild.channels, id=837714802049679451)
        staff_log_messageing_3 = discord.Embed(
            title="Moondog Logistics Applications | `apply` Logging Message", description=f"{ctx.author.name} Tried to apply to join the vtc tho there attempt was blocked because `They had the role name` **`Staff Team`**", color=0xFF0000)
        staff_log_messageing_3.set_footer(
            text=f"Moondog Logistics Applications | Apply Logging Message â€¢ {time_main2}")
        await channel1.send(embed=staff_log_messageing_3)

    await asyncio.sleep(20)

    def check(message):
        return message.author == ctx.author and message.channel == ticket_channel
    await ticket_channel.send(f"{ctx.author.mention}")
    try:
     question1_em = discord.Embed(
         title="Moondog Logistics Applications | Question 1 ", description=f"Hey, {ctx.author.name} what is your name?", color=0xFF0000)
     question1_em.set_footer(
         text=f"Moondog Logistics Applications | Question 1 â€¢ {time_main2}")
     remove1 = await ticket_channel.send(embed=question1_em)
     msg = await bot.wait_for('message', check=check, timeout=3600)
     response = (msg.content)
    except asyncio.TimeoutError:
        em = discord.Embed(
             title="Moondog Logistics Applications", description=f"Hey {ctx.author.name}, are you there? You opened up a application @ Moondog Logistics and have not answered any of the questions after 1hr.", color=0x00a8ff)
        await asyncio.sleep(3600)
        await ctx.author.send(embed=em)
        try:
             question1_em = discord.Embed(
                 title="Moondog Logistics Applications | Question 1 ", description=f"Hey, {ctx.author.name} what is your name?", color=0xFF0000)
             question1_em.set_footer(
                 text=f"Moondog Logistics Applications | Question 1 â€¢ {time_main2}")
             remove1 = await ticket_channel.send(embed=question1_em)
             msg = await bot.wait_for('message', check=check, timeout=7200)
             response = (msg.content)
        except:
                em2 = discord.Embed(
                    title="Moondog Logistics Applications", description=f"Hey {ctx.author.name}, Your application with Moondog Logistics will be closed in 5 mins as you have not responded to any of the questions in 2hrs", color=0x00a8ff)
                await asyncio.sleep(3600)
                await ctx.author.send(embed=em2)
                await asyncio.sleep(300)
                await ticket_channel.delete()
                await ctx.author.send(f"{ctx.author.name} Your Application Has been closed.")
                role = discord.utils.get(
                      ctx.guild.roles, id=837608034721071104)
                await ctx.author.remove_roles(role)
                index = data["ticket-channel-ids"].index(ticket_channel.id)
                del data["ticket-channel-ids"][index]
                with open('data.json', 'w') as f:
                   json.dump(data, f)
                mydb = mysql.connector.connect(
                      host="localhost",
                      user="root",
                      password="Fv4&4*JT61%8WGj&vwj",
                      database="alleapi"
                  )
                mycursor = mydb.cursor()
                sql = f"UPDATE applications SET status = 'Closed', statusaddedby = '{ctx.author}' WHERE id = '{id}'"
                mycursor.execute(sql)
                mydb.commit()
    question2_em = discord.Embed(
        title="Moondog Logistics Applications | Question 2 ", description=f"Hey, {ctx.author.name} what is your TMPID?", color=0xFF0000)
    question2_em.set_footer(
        text=f"Moondog Logistics Applications | Question 2 â€¢ {time_main2}")
    remove2 = await ticket_channel.send(embed=question2_em)
    msg2 = await bot.wait_for('message', check=check)
    response2 = (msg2.content)
    # question 3 removed due to no longer being needed
    question3_em = discord.Embed(
        title="Moondog Logistics Applications | Question 3 ", description=f"Hey, {ctx.author.name} what country are you from?", color=0xFF0000)
    question3_em.set_footer(
        text=f"Moondog Logistics Applications | Question 3 â€¢ {time_main2}")
    remove3 = await ticket_channel.send(embed=question3_em)
    msg4 = await bot.wait_for('message', check=check)
    response4 = (msg4.content)
    question4_em = discord.Embed(
        title="Moondog Logistics Applications | Question 4 ", description=f"Hey, {ctx.author.name} what is your age?", color=0xFF0000)
    question4_em.set_footer(
        text=f"Moondog Logistics Applications | Question 4 â€¢ {time_main2}")
    remove4 = await ticket_channel.send(embed=question4_em)
    msg5 = await bot.wait_for('message', check=check)
    response5 = (msg5.content)

    #checks if they are older then
    #if msg5.content < 16:
    #your_not_old_enough = discord.Embed(
    #  title="Moondog Logistics Applications | Age Check ", description=f"Hey, {ctx.author.name} your application has been **`Automatically Denied`** as you are under the age of 16.", color=0xFF0000)
    #your_not_old_enough.set_footer(
    #text="Moondog Logistics Applications | Age Check â€¢ 2021")
    #await ctx.author.send(embed=your_not_old_enough)
    #   await ticket_channel.delete()
    #role = discord.utils.get(ctx.guild.roles, id=837608034721071104)
    #await ctx.author.remove_roles(role)
    #index = data["ticket-channel-ids"].index(ticket_channel.id)
    #del data["ticket-channel-ids"][index]
    #with open('data.json', 'w') as f:
    #json.dump(data, f)
    #mydb = mysql.connector.connect(
    #host="localhost",
    # user="root",
    #   password="Fv4&4*JT61%8WGj&vwj",
    #  database="alleapi"
    #)
    #mycursor = mydb.cursor()
    #sql = f"UPDATE applications SET status = 'Closed / Under Age', statusaddedby = '{ctx.author}' WHERE id = '{id}'"
    #mycursor.execute(sql)
    #mydb.commit()
    timestamp = datetime.now(pytz.timezone("Europe/London"))
    
    Diretor_role2 = discord.utils.get(ctx.guild.roles, id=837606126795227136)
    await ticket_channel.send(f"{Diretor_role2.mention} New application finshed. The answers are below!!")
    thanks_for_answering_alle_questions = discord.Embed(title="Moondog Logistics Applications | Your Application Has Been Recived.",
                                                        description=f"Hey {ctx.author.name}, Thanks for answering all the questions a member of staff will now deal with your application. **Please remember it can take up to 2 days for your application to be viewed.**", color=0xFF0000)
    thanks_for_answering_alle_questions.set_footer(
        text=f"Moondog Logistics Applications | Applications System â€¢ {time_main2}")
    await ctx.author.send(embed=thanks_for_answering_alle_questions)
    questionr = discord.Embed(title="Moondog Logistics Applications | Answers To Application Questions",
                              description=f"Here are the answers to the application questions:", color=0xFF0000)
    questionr.add_field(name="Name", value=f"{response}", inline=True)
    questionr.add_field(name="TMPID", value=f"{response2}", inline=True)
    questionr.add_field(name="Country", value=f"{response4}", inline=True)
    questionr.add_field(name="Age", value=f"{response5}", inline=True)
    questionr.add_field(name="Applicant's Discord:",
                        value=f"{ctx.author}", inline=True)
    questionr.add_field(name="Application Submitted:", value=timestamp.strftime(
        r"On: %d/%m/%Y At: %I:%M %p"), inline=True)
    questionr.set_footer(
        text=f"Moondog Logistics Applications | Applications System â€¢ {time_main2}")
    await ticket_channel.send(embed=questionr)
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Fv4&4*JT61%8WGj&vwj",
        database="alleapi"
    )
    mycursor = mydb.cursor()

    day = dt.now()
    sql = "INSERT INTO  applications(discordname, applicationdate, applicationid, status, statusaddedby, tmpid) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (f"{ctx.author.name}#{ctx.author.discriminator}",
           f"{day}", f"{ticket_number}", f"Sent", f"applications bot", f"{response2}")
    mycursor.execute(sql, val)
    mydb.commit()
    await remove1.delete()
    await remove2.delete()
    await remove3.delete()
    await remove4.delete()

    await msg.delete()
    await msg2.delete()
    await msg4.delete()
    await msg5.delete()
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Fv4&4*JT61%8WGj&vwj",
        database="alleapi"
    )
    cursor = mydb.cursor()
    cursor.execute(
        f"SELECT  discordid FROM blacklist WHERE discordid = '{ctx.author.id}'")
    results = cursor.fetchall()
    # gets the number of rows affected by the command executed
    row_count = cursor.rowcount
    if row_count > 0:
        Member_already_blacklisted = discord.Embed(
            title="Moondog Logistics Applications | `blacklist` error", description=f"That person is already blacklisted. DiscordID: {ctx.author.id}", color=0xFF0000)
        await ticket_channel.send(embed=Member_already_blacklisted)
        you_are_blacklisted = discord.Embed(
            title="Moondog Logistics Applications | Blacklist System", description=f"Your application with Moondog Logistics has been **Automatically Denied** because  you are **blacklisted** from applying. If you attempt to evade this then you will be banned.", color=0xFF0000)
        you_are_blacklisted.set_footer(
            text=f"Moondog Logistics Applications | Blacklist System â€¢ {time_main2}")
        await ctx.author.send(embed=you_are_blacklisted)

        await ticket_channel.delete()
        role = discord.utils.get(ctx.guild.roles, id=837608034721071104)
        await ctx.author.remove_roles(role)
        index = data["ticket-channel-ids"].index(ticket_channel.id)
        del data["ticket-channel-ids"][index]
        with open('data.json', 'w') as f:
         json.dump(data, f)
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Fv4&4*JT61%8WGj&vwj",
            database="alleapi"
        )
        mycursor = mydb.cursor()
        sql = f"UPDATE applications SET status = 'Closed', statusaddedby = '{ctx.author}' WHERE id = '{id}'"
        mycursor.execute(sql)
        mydb.commit()

    try:
     getplayerinfourl = f"https://api.truckersmp.com/v2/player/{response2}"
     r = requests.get(getplayerinfourl)
     data = r.json()["response"]
     hook = Webhook(
         'https://discord.com/api/webhooks/843949554738135091/gFJX3o2BTLPK2758j0G3t-ZtNDL8Yx4Md_S05ImrW6sBCIQrB-WuOo-L3zUUInpRQY3V')
     for server in data:
      em2 = discord.Embed(title="Player lookup (tmp)",
                          url=f"https://truckersmp.com/user/{response2}", color=0x00FF00)
      em2.set_thumbnail(
          url=data["avatar"])
      em2.add_field(name="Name", value=data["name"], inline=True)
      em2.add_field(name="Tmp id", value=data["id"], inline=True)
      em2.add_field(name="Steam id", value=data["steamID64"], inline=True)
      em2.add_field(name="Banned", value=data["banned"], inline=True)
      em2.add_field(name="Banned until",
                    value=data["bannedUntil"], inline=True)
      em2.add_field(name="Bans count", value=data["bansCount"], inline=True)
      em2.add_field(name="Join Date", value=data["joinDate"], inline=True)
      em2.add_field(name="Discord User ID",
                    value=data["discordSnowflake"], inline=True)
      em2.add_field(name="Applicants Discord Name And ID",
                    value=f"{ctx.author.name} & {ctx.author.id}")
     hook.send(embed=em2)
     in_a_vtc_check = (data["vtc"]["inVTC"])
     if in_a_vtc_check == True:
        in_a_vtc_true = discord.Embed(title="Moondog Logistics Applications| Application System",
                                      description=f"Hey {ctx.author.name}, Your already in a vtc. We dont allow dual vtcing. If you wish to join Moondog Logistics please leave this vtc and then we can carry on with your application. You will have 1hr to do this. Then your application channel will be Automatically closed after the bot checks for one more time.", color=0xFF0000)
        in_a_vtc_true.set_footer(
            text="Moondog Logistics Applications| Application System")
        await ctx.author.send(embed=in_a_vtc_true)

        this_user_is_in_a_vtc = discord.Embed(title="Moondog Logistics Applications| Application System",
                                              description=f"Hey Moondog, the user {ctx.author.name} is already in vtc. They have been given 1hr to leave.", color=0xFF0000)
        this_user_is_in_a_vtc.set_footer(
            text="Moondog Logistics Applications| Application System")
        await hook.send(embed=this_user_is_in_a_vtc)
        channel = discord.utils.get(ctx.guild.channels, id=837714802049679451)
        await ticket_channel.send(f"Hey staff member please make sure to check this channel {channel.mention}")

     banned = (data["banned"])
     if banned == False:
        bannedem = discord.Embed(
            title=f":green_circle: {ctx.author} is **not** currently  banned. :green_circle: ", color=0x00FF00)
        hook.send(embed=bannedem)
     else:
        bannedem = discord.Embed(
            title=f":warning: {ctx.author} is currently banned. Until:" + data["bannedUntil"] + ":warning:", color=0x00FF00)
        hook.send(embed=bannedem)
     if banned > 2 and banned < 5:
        banned4 = f"{ctx.author.mention} HAS MORE THEN 2 BANS BUT IS LESS THEN 5"
        hook.send(banned4)
     else:
        banned5 = f"{ctx.author.mention} HAS LESS THEN 2 BANS"
        hook.send(banned5)
     if banned == 5:
        hook3 = webhook(
            'https://discord.com/api/webhooks/843949554738135091/gFJX3o2BTLPK2758j0G3t-ZtNDL8Yx4Md_S05ImrW6sBCIQrB-WuOo-L3zUUInpRQY3V'
        )
        em34 = discord.Embed(title=f":warning: DRIVER IS PERM BANNED :warning:", description=f"Someone has tired to apply when they are perm banned on TMP this was dected by Moondogs auto ban detection system. Drivers info TMP Name:" +
                             data["name"] + "" f"Discord Name and ID: {ctx.author} {ctx.author.id}" + "" + "TMP ID:" + "" + data["id"])
        hook3.send(embed=em34)
        await ctx.channel.delete()
        role = discord.utils.get(ctx.guild.roles, name="Applicant")
        await ctx.author.remove_roles(role)
        index = data["ticket-channel-ids"].index(ticket_channel.id)
        del data["ticket-channel-ids"][index]

        with open('data.json', 'w') as f:
            json.dump(data, f)
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Fv4&4*JT61%8WGj&vwj",
            database="alleapi"
        )
        mycursor = mydb.cursor()
        sql = f"UPDATE applications SET status = 'Closed', statusaddedby = '{ctx.author}' WHERE id = '{id}'"
        mycursor.execute(sql)
        mydb.commit()
        hook1 = Webhook(
            'https://discord.com/api/webhooks/827502772291239996/sH6UfgNFrVvKwAbdsFH2svKOGSEgHNhxwZ7V8UHyWikR3O4bFxID5QwSxNx3XKQcRq7c')
        userapplyed = discord.Embed(title="Moondog Logistics Applications",
                                    description=f"Updated Mysql applications to 'closed'.")
        hook1.send(embed=userapplyed)
        hook1.send(
            f"{ticket_channel.mention} has been removed as the user had 5 bans.")
        ctx.author.send("Your application with Moondog Logistics has been canceled. Reason: `5 bans or more` **This is a auto system action if this is wrong please contact a member of the upper staff team**")
        # Checks if user is already blacklisted (checks by discordID)

     else:
         pass
         print("channel not removed")

    except:
        em3 = discord.Embed(title="Player lookup (tmp) Error",
                            description="we could not lookup this user", color=0xFF0000)
        hook.send(embed=em3)
        error34 = discord.Embed(title="Moondog Logistics Applications",
                                description=f"The TMPID you gave does not seem to exist  TMPID = {response2}")
        await ticket_channel.send(embed=error34)

    warningmsg = discord.Embed(title="Moondog Logistics Applications",
                               description=f"To see the status of your application do `a/status id` your Application ID is {ticket_number}")
    await asyncio.sleep(60)
    await ticket_channel.send(embed=warningmsg)


@apply.error
async def apply_handler_command_cooldown(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"{ctx.author.mention}")
        global time_main2
        # sends error if the command has not be used in a application ticket channel.
        apply_on_cooldown = discord.Embed(title="Moondog Logistics Applications | `apply` error",
                                          description=f"Im sorry but at this time this command is on a cooldown please try again in {error.retry_after:.2f}s", color=0xFF0000)
        apply_on_cooldown.set_footer(
            text=f"Moondog Logistics Applications |  apply error message â€¢ {time_main2}")
        await ctx.send(embed=apply_on_cooldown)


@bot.command()
async def close(ctx, id, user: discord.Member):
    await ctx.message.delete()
    with open('data.json') as f:
        data = json.load(f)

    if ctx.channel.id in data["ticket-channel-ids"]:

        channel_id = ctx.channel.id

        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel and message.content.lower() == "close"

        try:

            em = discord.Embed(
                title="Moondog Logistics Applications", description="Are you sure you want to close this ticket? Reply with `close` if you are sure.", color=0x00a8ff)

            await ctx.send(embed=em)
            await bot.wait_for('message', check=check, timeout=60)
            await ctx.channel.delete()
            role = discord.utils.get(ctx.guild.roles, name="Applicant")
            await user.remove_roles(role)
            index = data["ticket-channel-ids"].index(channel_id)
            del data["ticket-channel-ids"][index]

            with open('data.json', 'w') as f:
                json.dump(data, f)
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Fv4&4*JT61%8WGj&vwj",
                database="alleapi"
            )
            mycursor = mydb.cursor()
            sql = f"UPDATE applications SET status = 'Closed', statusaddedby = '{ctx.author}' WHERE applicationid = '{id}'"
            mycursor.execute(sql)
            mydb.commit()
            hook = Webhook(
                'https://discord.com/api/webhooks/827502772291239996/sH6UfgNFrVvKwAbdsFH2svKOGSEgHNhxwZ7V8UHyWikR3O4bFxID5QwSxNx3XKQcRq7c')
            userapplyed = discord.Embed(title="Moondog Logistics Applications",
                                        description=f"Updated Mysql applications to 'closed'.")
            hook.send(embed=userapplyed)
            role = discord.utils.get(ctx.guild.roles, name="Applicant")
            await ctx.author.remove_roles(role)
            hook = Webhook(
                'https://discord.com/api/webhooks/827502772291239996/sH6UfgNFrVvKwAbdsFH2svKOGSEgHNhxwZ7V8UHyWikR3O4bFxID5QwSxNx3XKQcRq7c')
            now = datetime.now(pytz.timezone("Europe/London"))
            userapplyed = discord.Embed(title="Moondog Logistics Applications",
                                        description=f"{ctx.author.mention} Has closed Application {id} @ {now}")
            hook.send(embed=userapplyed)
        except asyncio.TimeoutError:
            em = discord.Embed(
                title="Moondog Logistics Applications", description="You have run out of time to close this ticket. Please run the command again.", color=0x00a8ff)
            await asyncio.sleep(60)
            await ctx.send(embed=em)
    else:
        # sends error if the command has not be used in a application ticket channel.
        not_a_ticket_channel = discord.Embed(title="Moondog Logistics Applications | `close` error",
                                             description="This command can only be used in a application channel.", color=0xFF0000)
        await ctx.send(embed=not_a_ticket_channel)


@close.error
async def close_handler_missing_arg(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        # sends error if the command has not be used in a application ticket channel.
        provide_args = discord.Embed(title="Moondog Logistics Applications | `close` error",
                                     description="Please include `id` and `member` at the end of the command `a/close`", color=0xFF0000)
        await ctx.send(embed=provide_args)


@close.error
async def close_handler(ctx, error):
    if isinstance(error, commands.BadArgument):
        no_member = discord.Embed(title="Moondog Logistics Applications | `close` error",
                                  description="I cant find that member in this guild :(", color=0xFF0000)
        await ctx.send(embed=no_member)


@bot.command()
async def hire(ctx, id, tmpid,  member: discord.Member):
  role = discord.utils.get(ctx.guild.roles, id=837606126795227136)
  if role in ctx.author.roles:
    await ctx.message.delete()
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Fv4&4*JT61%8WGj&vwj",
        database="alleapi"
    )
    mycursor = mydb.cursor()
    sql = f"UPDATE applications SET status = 'Hired', statusaddedby = '{ctx.author}' WHERE applicationid = '{id}'"
    mycursor.execute(sql)
    mydb.commit()
    with open('data.json') as f:
        data = json.load(f)

    if ctx.channel.id in data["ticket-channel-ids"]:

        channel_id = ctx.channel.id

        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel and message.content.lower() == "yes"

        try:

            em3445 = discord.Embed(
                title="Moondog Logistics Applications", description="Are you sure you want to hire this driver? Reply with `yes` if you are sure.", color=0x00a8ff)
            await ctx.send(embed=em3445)
            await bot.wait_for('message', check=check, timeout=60)
            index = data["ticket-channel-ids"].index(channel_id)
            del data["ticket-channel-ids"][index]

            with open('data.json', 'w') as f:
                json.dump(data, f)
            role = discord.utils.get(ctx.guild.roles, name="Applicant")
            role2 = discord.utils.get(
                ctx.guild.roles, name="Probationary Driver")
            await member.remove_roles(role)
            await member.add_roles(role2)

            hook = Webhook(
                'https://discord.com/api/webhooks/827502772291239996/sH6UfgNFrVvKwAbdsFH2svKOGSEgHNhxwZ7V8UHyWikR3O4bFxID5QwSxNx3XKQcRq7c')
            info1 = discord.Embed(title="Moondog Logistics Applications",
                                        description=f"Updated **mysql** table `applications` SET status of application {id} to `hired`")
            hook.send(embed=info1)
            getinfourl = f"https://api.truckersmp.com/v2/player/{tmpid}"
            r = requests.get(getinfourl)
            data = r.json()["response"]
            cursor = mydb.cursor()
            sql = "INSERT INTO drivers (name, discordname, tmpid, steamid, role) VALUES (%s, %s, %s, %s, %s)"
            val = (data["name"], f"{member}", f"{tmpid}",
                   data["steamID64"], f"Probationary Driver")
            cursor.execute(sql, val)
            mydb.commit()
            await member.send(f"{ctx.author} just updated your application at Moondog Logistics to `Hired`")
            await member.send("Welcome to Moondog Logistics Your role is `Probationary Driver`")
            channel1 = bot.get_channel(797186729232433193)
            #await channel1.send(f"Welcome to Moondog Logistics {member.mention}. Please Book your training here https://alle-group.com/book-training/")
            hook = Webhook(
                'https://discord.com/api/webhooks/822167721016819716/nQRa4Eehf-DRFQuFTEdoqSs6_7t3h5miB5LOGwahyM2NJLDcsHmMWm4488cIAGeMSmC_')
            em2 = discord.Embed(
                title=f"{member} has been promoted to Probationary Driver", description="")
            #hook.send(embed=em2)
            userapplyed = discord.Embed(title="Moondog Logistics Applications",
                                        description=f"{ctx.author.mention} Hired {member.mention}")
            #hook.send(embed=userapplyed)
            await ctx.send("Driver added to our database and to our company")
            await ctx.channel.delete()

            try:
                role1 = discord.utils.get(
                    ctx.guild.roles, id=837666217413967882)
                role2 = discord.utils.get(
                    ctx.guild.roles, id=837607050417537045)
                role3 = discord.utils.get(
                    ctx.guild.roles, id=837608034721071104)
                hours = 60*60
                await asyncio.sleep(3628800)
                await member.remove_roles(role3)
                await member.add_roles(role1)
                await member.add_roles(role2)
                joined_server = member.joined_at.strftime("%b %d, %Y")
                await member.send(f"Hey, your probation period is up congrats. You have been in Moondog Logisticss Discord server since: {joined_server}")
            except:
                await ctx.send("oh it did not work")

            # Adding in #staff-logs logging for this bot!
            try:
                hire_log_msg = discord.Embed(
                    title="Moondog | Applications", description=f"New driver hired by {ctx.author.mention} | Addded to the company api and database | Please add to the staff hub (coming soon!!)")
                staff_logs_channel = bot.get_channel(837715287092232264)
                await staff_logs_channel.send(embed=hire_log_msg)

            except:
                hire_log_err_msg = discord.Embed(
                    title="Moondog | Applications | Error", descrition=f"Error could not send the log message to {staff_logs_channel.mention}.")
                await ctx.author.send(embed=hire_log_err_msg)

            # Add to staff hub message (send in dms).
            try:
                advice_msg = discord.Embed(
                    title="Moondog | Applications", descrition=f"{member} | has been hired. | Please add them to the staff hub.")
                await ctx.author.send(embed=advice_msg)

            except:
                advice_msg_error = discord.Embed(
                    title="Moondog | Applications", descrition=f"{ctx.author.mention} I tried to send you a msg in dms but i could not. pepesad")
                main_chat_channel = bot.get_channel(837713193672900688)
                await ctx.main_chat_channel.send(embed=advice_msg_error)

         #this will happen if it times out after 60 secs
        except asyncio.TimeoutError:
            em = discord.Embed(
                title="Moondog Logistics Applications", description="You have run out of time to hire this driver. Please run the command again.", color=0x00a8ff)
            await ctx.send(embed=em)
    else:
        # sends error if the command has not be used in a application ticket channel.
        not_a_ticket_channel = discord.Embed(title="Moondog Logistics Applications | `hire` error",
                                             description="This command can only be used in a application channel.", color=0xFF0000)
        await ctx.send(embed=not_a_ticket_channel)
  else:
      errormsg = discord.Embed(
          title="Moondog Logistics applications", description="You do not have the correct roles or perms to use the command `hire`", color=0xFF0000
      )
      await ctx.send(embed=errormsg)


@hire.error
async def hire_handler(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
       forgotiderr = discord.Embed(
           title="Moondog Logistics Applications | `hire` error", description=f"This command requires the following arguments `id` `tmpid` `member` one of these are not present in your command `(a/hire application-id, tmpid, member(discord ping))`", color=0xFF0000)
    await ctx.send(embed=forgotiderr)


@hire.error
async def hire_handler2(ctx, error):
    if isinstance(error, commands.BadArgument):
        no_member = discord.Embed(title="Moondog Logistics Applications | `close` error",
                                  description="I cant find that member in this guild :(", color=0xFF0000)
        await ctx.send(embed=no_member)
