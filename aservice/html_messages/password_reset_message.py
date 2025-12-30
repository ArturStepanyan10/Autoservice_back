def get_password_reset_html_message(reset_code):
    html_message = f"""
                  <html>
                     <body style="font-family: Arial, sans-serif; line-height: 1.6; padding: 20px; 
                                                                                    text-align: justify;">
                         <p>Здравствуйте!</p>
    
                         <p>Чтобы сбросить пароль от аккаунта на AutoMaster Autoservice, пропишите код в приложении,
                         который ниже указан.</p>
    
                         <p style="font-size: 15px; color: blue; text-decoration: underline;">
                             {reset_code}
                         </p>
    
                         <p>Если вы не запрашивали изменение пароля, пожалуйста, проигнорируйте это сообщение.</p>
    
                         <p>Команда Autoservice AutoMaster!</p>
                     </body>
                 </html>
    """
    return html_message
