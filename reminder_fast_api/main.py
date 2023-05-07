from datetime import datetime
from uuid import uuid4
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette import status
from starlette.templating import Jinja2Templates

app = FastAPI()
app.secret_key = str(uuid4())

templates = Jinja2Templates(directory='templates')

reminders = []


@app.get('/', response_class=HTMLResponse)
@app.post('/', response_class=HTMLResponse)
async def home(request: Request):
    if request.method == 'POST':
        form = await request.form()
        text = form['reminder']
        date = form['date']
        time = form['time']

        date_str = f'{date} {time}'
        date_obj = datetime.strptime(date_str, '%Y-%M-%D %H:%M')

        reminders.append(
            {
                'text': text,
                "date": date_obj
            }
        )
        return RedirectResponse(url='/', status_code=status.HTTP_303_SEE_OTHER)
    now = datetime.now()
    upcoming_reminders = list()
    for index,reminder in enumerate(reminders):
        if reminder['date'] > now:
            reminder['index'] = index
            upcoming_reminders.append(reminder)
    return templates.TemplateResponse('home.html',
                                      {
                                          'upcoming_reminders': upcoming_reminders,
                                          'request': request
                                      }
                                      )
@app.post('/delete/{index}')
async def delete_reminder(index: int):
    reminders.pop(index)
    return RedirectResponse('/',status_code=status.HTTP_303_SEE_OTHER)
