from front_ex import create_user
import json
from flask import render_template, request, jsonify, redirect
from flask.helpers import url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, DateField, SelectMultipleField 
from wtforms import SubmitField, TextAreaField, SelectField, IntegerField, FieldList
from wtforms.validators import DataRequired, Length, InputRequired, Email, NumberRange, EqualTo, Optional
from wtforms.fields.html5 import DateField, EmailField
from wtforms.widgets import TextInput
# from flask_admin.form.fields import Select2TagsField

import requests

from flask_restful import Resource, reqparse 
import pandas as pd
import numpy as np
from io import BytesIO
from flask import send_file

from . import app
from .utils import TagListField
from . import api
# Уточнить по чему в данном случае не работает относительная ссылка
import front_ex.config as config


from .utils import get_sap_s4_con_str, get_postgre_con_str
from sqlalchemy import create_engine

class Select2MultipleField(SelectMultipleField):
    def pre_validate(self, form):
        # Prevent "not a valid choice" error
        pass

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = ",".join(valuelist)
        else:
            self.data = ""

# Форма настройки
class Report1_Form(FlaskForm):
    """Форма настройки отчета"""
    date_from = DateField('Дата с')
    date_to = DateField('Дата по')
    # tor = TagListField('Вид ТОР', pl choices=[('113','113'),('710','710'),('122','122'),('124','124'),('730','730')])
    tor = Select2MultipleField('Вид ТОР:', choices=[('113','113'),('710','710'),('122','122'),('124','124'),('730','730')]\
    #     , render_kw={"multiple": "multiple", "data-tags": "1"})
        , render_kw={"multiple": "multiple", "data-tags": "1"})
    submit = SubmitField('Выгрузить')

# front-end настройка запроса
@app.route('/reports/tor_1', methods=['GET', 'POST'])
def reports_report1(redirect=None):
    form = Report1_Form()
    # user = User.query.filter_by(id=id).first_or_404()
    # form = ProfileEditForm(user.email)

    if form.validate_on_submit():
        # redirect_url = "http://{host}:{port}/api/{report}?datefrom={datefrom}&dateto={dateto}"\
        #         .format(host=config.BACKEND_SERVICE_HOST\
        #         , port=config.FLASK_PORT, report='report1', datefrom=form.date_from.data, dateto=form.date_to.data)

        redirect_url = "http://{host}:{port}/api/{report}?datefrom={datefrom}&dateto={dateto}"\
            .format(host=config.BACKEND_SERVICE_HOST\
            , port=config.FLASK_PORT, report='report1', datefrom=form.date_from.data, dateto=form.date_to.data)
        
        try:
            return render_template('/reports/download.html',redirect_url=redirect_url)
        except Exception:
            return "Error with {}".format(redirect_url)
    elif request.method == 'GET':
        form.name = 'report1'
    else:
        print(form.errors)
        data = json.dumps(form.errors, ensure_ascii=False)
        return jsonify(data)
    return render_template('/reports/settings.html', title="Редактирование", form=form)

# REST API класс выгрузки отчета
# Выгрузка отчетов\


class Report11(Resource, debug=False):
    def get(self, debug=False):

        print(request.args.get('datefrom'),request.args.get('dateto'))
        redirect_url = request.args.get('redirect')

        engine_sap_s4 = create_engine(get_sap_s4_con_str(), max_identifier_length=128)
        engine_postgre = create_engine(get_postgre_con_str(), max_identifier_length=128, encoding='utf-8')

        if config.DEBUG:
            print('1. Загрузка данных по ТОР')

        sql = """ 
            select t.auart "Вид заказа"
                ,t.autyp "Тип заказа"
                ,t.ilart "Вид работы ТОРО"
                ,t.ilatx "Название ВРТ"
                ,t.equnr  "Ед. оборудования"
                ,t.iloan "Мстплж/Контир"
                ,t.iwerk "Планир. завод"
                ,t.ingpr "ГрупПлановик"
                ,t.pm_objty "Тип объекта"
                ,t.obknr "СписОбъект"
                ,t.gewrk "Рабочее место"
                ,t.vatxt "Описание"
                ,t.qmnum "Сообщение"
                ,t.ernam "Создатель"
                ,to_date(t.erdat,'YYYYMMDD') "Дата ввода"
                ,to_date(t.gstrp,'YYYYMMDD') "Базисный срок начала"
                ,t.gltrp "Базисный срок конца"
                ,t.ftrmi "ФактичСрокДеблокиров"
                ,a.bldat "Дата документа"
                ,nrp.datnrp "Дата перевода в НРП"
                ,rp.datrp "Дата перевода в РП"
                ,t.ktext "Краткий текст"
                ,t.serialnr "Серийный номер"
                ,t.sermat "Материал"
                ,m.maktx "Наименование материала"
                ,t.eqktx "Название объекта"
                ,case when w.OWNERTYPE = '0' then 'вагон не в аренде'
                when w.OWNERTYPE = '1' then 'собственный' 
                when w.OWNERTYPE = '2' then 'арендованный'
                when w.OWNERTYPE = '3' then 'инвентарный' end "Тип владения"
                ,t.anlnr "Основное средство"
                ,t.tplnr "Техническое место"
                ,i.pltxt "Наименование тех места"
                ,t.rsnum "Резервирование"
                ,t.gamng "Общий объем заказа"
                ,q.fegrp "Группа кодов"
                ,q.KURZTEXT "Группа кодов_текст"
                ,q.fecod "Код повреждения"
                ,q.KURZTEXT2 "Код повреждения_текст"
                ,t.objnr "Номер объекта"
                ,af.ebeln "Заказ на поставку"
                ,ek.IHREZ "Договор RCM"
                ,zc.RCM_DOGNUM "Договор"
                ,j.ptxt04 "Пользовательский статус"
                ,j.sstat "Системный статус"
                ,a.RACCT "Счет"
                ,a1.txt50 "Наименование счета"
                ,a.WSL "Сумма" 
                from sapabap1."ZVPM_R465" t --основная табличка
                left join sapabap1."MAKT" m on m.matnr = t.sermat
                left join sapabap1."IFLO" i on i.tplnr = t.tplnr

                left join (select
                                distinct(tq.qmnum) as qmnum
                                ,string_agg(tq.fegrp,', ') as fegrp 
                                ,string_agg(tq.KURZTEXT,', ') as KURZTEXT 
                                ,string_agg(tq.fecod,', ') as fecod
                                ,string_agg(tq.KURZTEXT2,', ') as KURZTEXT2 
                                from
                                (select
                                        t1.qmnum
                                        ,t1.fegrp
                                        ,t2.KURZTEXT 
                                        ,t1.fecod 
                                        ,p.KURZTEXT as KURZTEXT2
                                from sapabap1."VIQMFE" t1
                                left join sapabap1."QPGT" t2 on t2.CODEGRUPPE = t1.fegrp and t2.sprache = 'R'
                                left join sapabap1."QPCT" p on p.CODEGRUPPE = t1.fegrp and p.CODE = t1.fecod) tq group by tq.qmnum) q on q.qmnum = t.qmnum
                left join (select 
                                a.aufnr
                                ,max(a.ebeln) as ebeln
                                from sapabap1."AUFM" a
                                group by a.aufnr) af on af.aufnr = t.aufnr

                left join sapabap1."EKKO" ek on ek.ebeln = af.ebeln
                left join sapabap1."ZIRCM_CONTR" zc on zc.EXT_KEY = ek.ihrez
                left join (select 
                                distinct(z1.aufnr)
                                ,to_date(z1.DAT_PROCESS) as datnrp 
                                from sapabap1."ZTPM_CLEAR_1353" z1 
                                where z1.KSOOB = '5353') nrp on nrp.aufnr = t.aufnr  
                left join (select 
                                distinct(z2.aufnr)
                                ,to_date(z2.DAT_PROCESS) as datrp 
                                from sapabap1."ZTPM_CLEAR_1353" z2 
                                where z2.KSOOB = '5354') rp on rp.aufnr = t.aufnr 
                left join sapabap1."ZTPM_WAG_GEN" w on w.equnr = t.equnr and w.DATBI = '99991231'

                left join (select
                                j.objnr
                                ,jp.ptxt04 
                                ,j.sstat
                            from (select
                                            distinct(j2.objnr) as objnr
                                            ,string_agg(j2.stxt04,',') as sstat
                                        from 
                                                (select
                                                    j1.objnr
                                                    ,j1.stat
                                                    ,js.stsma
                                                    ,tj.txt04 as stxt04
                                                from sapabap1."JEST" j1
                                                left  join sapabap1."JSTO" js on js.objnr = j1.objnr
                                                left join sapabap1."TJ02T" tj on tj.istat = j1.stat and tj.spras = 'R' 
                                                where j1.objnr like 'OR%'
                                                and j1.stat like 'I%'
                                                and j1.inact <> 'X') j2 group by j2.objnr) j
                            join (select distinct(j1.objnr) as objnr
                                                ,j1.stat
                                                ,js.stsma
                                                ,jt.txt04 as ptxt04
                                                from sapabap1."JEST" j1
                                                left  join sapabap1."JSTO" js on js.objnr = j1.objnr
                                                left  join sapabap1."TJ30T" jt on jt.estat = j1.stat and jt.spras = 'R' and jt.stsma = js.stsma 
                                                where j1.objnr like 'OR%'
                                                and j1.stat like 'E%'
                                                and j1.inact <> 'X') jp on jp.objnr = j.objnr) j on j.objnr = t.objnr --статусы
                            
                left join sapabap1."ACDOCA" a on a.aufnr = t.aufnr and a.RLDNR = '0L' and a.VRGNG = 'COIN'
                left join sapabap1."SKAT" a1 on a1.SAKNR = a.racct

                --where t.ilart in ('113','710','122','124','730') --ТР1_ППВ
                --where t.ilart in ('114','720') --ТР2
                where t.ilart in ('113','114','710','720','122','124','730') -- ТР1, ТР2, ППВ
                and t.erdat between '20210101' and '20210331'

                group by t.aufnr,t.auart,t.autyp,t.ilart,t.ilatx ,t.equnr  ,t.iloan,t.iwerk ,t.ingpr,t.pm_objty,t.obknr,t.gewrk,t.vatxt
                ,t.qmnum,t.ernam,t.erdat,t.gstrp,t.gltrp,t.ftrmi, a.bldat, t.ktext,t.serialnr ,t.sermat ,m.maktx ,t.eqktx 
                ,t.anlnr,t.tplnr ,i.pltxt,t.rsnum ,t.gamng,q.fegrp ,q.KURZTEXT ,q.fecod ,q.KURZTEXT2 ,t.objnr 
                ,af.ebeln,ek.IHREZ,zc.RCM_DOGNUM,j.ptxt04 ,j.sstat,w.OWNERTYPE,nrp.datnrp,rp.datrp,a.RACCT,a.WSL,a1.TXT50
        """
        data = pd.read_sql(sql, engine_sap_s4)
        print(sql)
        #create a random Pandas dataframe
        df_1 = pd.DataFrame(np.random.randint(0,10,size=(10, 4)), columns=list('ABCD'))

        #create an output stream
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')

        #taken from the original question
        # df_1.to_excel(writer, startrow = 0, merge_cells = False, sheet_name = "Sheet_1")
        data.to_excel(writer, startrow = 0, merge_cells = False, sheet_name = "Sheet_1")

        workbook = writer.book
        worksheet = writer.sheets["Sheet_1"]
        format = workbook.add_format()
        format.set_bg_color('#eeeeee')
        worksheet.set_column(0,9,28)

        #the writer has done its job
        writer.close()

        #go back to the beginning of the stream
        output.seek(0)

        #finally return the file
        return send_file(output, attachment_filename="testing2.xlsx", as_attachment=True) 
        # return render_template('/reports/download.html')
api.add_resource(Report11, '/api/report1')