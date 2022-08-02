import os
import io
import sys
import pandas as pd
from helpers.bot_telegram import ChatTelegram


def path_temp():
    absolutepath = os.path.abspath(__file__)
    fileDirectory = os.path.dirname(absolutepath)
    file = os.path.join(fileDirectory, 'temp_file', 'Report.csv')
    return io.open(file, encoding='latin-1')


def separar_fecha(frame_matriz_filter, column, format):
    return pd.to_datetime(frame_matriz_filter[f'{column}'], format='%d/%m/%Y %H:%M').dt.strftime(f'{format}')


def filter_telegram(filter_frame, name_column):
    column_name = filter_frame.loc[:, name_column]
    space_values = ", ".join(column_name)
    return space_values


class ExtractData:
    def __init__(self, path_matriz):
        self.path_matriz = path_matriz

    def data_matriz(self, filter_hora, filter_date):
        df_matriz = pd.read_csv(self.path_matriz)
        frame_matriz = pd.DataFrame(df_matriz)
        frame_matriz_new = pd.DataFrame(frame_matriz, columns=[
            'ID del Cambio*+',
            'Estado*',
            'Clase*',
            'Resumen*',
            'Coordinador cambio*+',
            'Fecha programada de inicio+',
            'Fecha programada de finalización+',
            'Inicio Rollback',
            'Resp Otecel*'
        ])
        frame_matriz_filter = pd.DataFrame(frame_matriz, columns=[
            'ID del Cambio*+',
            'Estado*',
            'Clase*',
            'Resumen*',
            'Coordinador cambio*+',
            'Fecha programada de inicio+',
            'Fecha programada de finalización+',
            'Inicio Rollback',
            'Resp Otecel*'
        ])

        # Todo: Fecha programada de inicio
        date_programada = separar_fecha(frame_matriz_filter, 'Fecha programada de inicio+', '%d/%m/%Y')
        hour_programada = separar_fecha(frame_matriz_filter, 'Fecha programada de inicio+', '%H:%M')
        hour_convert_datetime64 = pd.to_datetime(hour_programada, format='%H:%M')
        hour_less_ten_minutes = hour_convert_datetime64 - pd.Timedelta(minutes=10)
        hour_convert_h_s = pd.to_datetime(hour_less_ten_minutes).dt.strftime('%H:%M')

        # Todo: Fecha programada finalizacion
        date_programada_final = separar_fecha(frame_matriz_filter, 'Fecha programada de finalización+', '%d/%m/%Y')
        hour_programada_final = separar_fecha(frame_matriz_filter, 'Fecha programada de finalización+', '%H:%M')
        hour_convert_datetime64_final = pd.to_datetime(hour_programada_final, format='%H:%M')
        hour_less_ten_minutes_final = hour_convert_datetime64_final - pd.Timedelta(minutes=10)
        hour_convert_h_s_final = pd.to_datetime(hour_less_ten_minutes_final).dt.strftime('%H:%M')

        # Todo: Fecha rollback
        date_programada_rollback = separar_fecha(frame_matriz_filter, 'Inicio Rollback', '%d/%m/%Y')
        hour_programada_rollback = separar_fecha(frame_matriz_filter, 'Inicio Rollback', '%H:%M')
        hour_convert_datetime64_rollback = pd.to_datetime(hour_programada_rollback, format='%H:%M')
        hour_less_ten_minutes_rollback = hour_convert_datetime64_rollback - pd.Timedelta(minutes=10)
        hour_convert_h_s_rollback = pd.to_datetime(hour_less_ten_minutes_rollback).dt.strftime('%H:%M')

        frame_add_colum = frame_matriz_new.assign(
            fecha_programada=date_programada,
            hora_programada=hour_convert_h_s,
            fecha_programada_final=date_programada_final,
            hora_programada_final=hour_convert_h_s_final,
            fecha_rollback=date_programada_rollback,
            hora_rollback=hour_convert_h_s_rollback
        )

        filter_hora_programada = frame_add_colum.loc[(frame_add_colum['hora_programada'] == filter_hora) &
                                                     (frame_add_colum['fecha_programada'] == filter_date)]

        filter_hora_programada_final = frame_add_colum.loc[(frame_add_colum['hora_programada_final'] == filter_hora) &
                                                           (frame_add_colum['fecha_programada_final'] == filter_date)]

        filter_hora_rollback = frame_add_colum.loc[(frame_add_colum['hora_rollback'] == filter_hora) &
                                                   (frame_add_colum['fecha_rollback'] == filter_date)]

        # # Todo: Filtro y envio de Hora programada Inicio
        id_cambio_inicio = filter_telegram(filter_hora_programada, 'ID del Cambio*+')
        estado_inicio = filter_telegram(filter_hora_programada, 'Estado*')
        clase_inicio = filter_telegram(filter_hora_programada, 'Clase*')
        resumen_inicio = filter_telegram(filter_hora_programada, 'Resumen*')
        coordinador_cambio_inicio = filter_telegram(filter_hora_programada, 'Coordinador cambio*+')
        fecha_programada_inicio = filter_telegram(filter_hora_programada, 'Fecha programada de inicio+')
        fecha_programada_fin_inicio = filter_telegram(filter_hora_programada, 'Fecha programada de finalización+')
        rollback_inicio = filter_telegram(filter_hora_programada, 'Inicio Rollback')
        resp_otecel_inicio = filter_telegram(filter_hora_programada, 'Resp Otecel*')

        if len(id_cambio_inicio) > 0:
            ChatTelegram(
                f'🔴 Inicio de actividad:\n{id_cambio_inicio},\n'
                f'🔴 con Estado:\n{estado_inicio},\n'
                f'🔴 Clase":\n{clase_inicio},\n'
                f'🔴 Resumen:\n{resumen_inicio},\n'
                f'🔴 Se inicia:\n{fecha_programada_inicio},\n'
                f'⚠️ Realiza las validaciones de alarmas previas y contacta al solicitante'
            )
        #
        # Todo: Filtro y envio de Hora programada Final
        id_cambio_final = filter_telegram(filter_hora_programada_final, 'ID del Cambio*+')
        estado_final = filter_telegram(filter_hora_programada_final, 'Estado*')
        clase_final = filter_telegram(filter_hora_programada_final, 'Clase*')
        resumen_final = filter_telegram(filter_hora_programada_final, 'Resumen*')
        coordinador_cambio_final = filter_telegram(filter_hora_programada_final, 'Coordinador cambio*+')
        fecha_programada_final = filter_telegram(filter_hora_programada_final, 'Fecha programada de inicio+')
        fecha_programada_fin_final = filter_telegram(filter_hora_programada_final, 'Fecha programada de finalización+')
        rollback_final = filter_telegram(filter_hora_programada_final, 'Inicio Rollback')
        resp_otecel_final = filter_telegram(filter_hora_programada_final, 'Resp Otecel*')

        if len(id_cambio_final) > 0:
            ChatTelegram(
                f'🔴 Fin de actividad:\n{id_cambio_final},\n'
                f'🔴 con Estado:\n{estado_final},\n'
                f'🔴 Clase:\n{clase_final},\n'
                f'🔴 Resumen:\n{resumen_final},\n'
                f'🔴 Finaliza":\n{fecha_programada_fin_final},\n'
                f'⚠️ Confirma la finalizacion y cambio de fase asi como la validacion de Alarmas post cambio'
            )

        # Todo: Filtro y envio de Hora programada Rollback
        id_cambio_rollback = filter_telegram(filter_hora_rollback, 'ID del Cambio*+')
        estado_rollback = filter_telegram(filter_hora_rollback, 'Estado*')
        clase_rollback = filter_telegram(filter_hora_rollback, 'Clase*')
        resumen_rollback = filter_telegram(filter_hora_rollback, 'Resumen*')
        coordinador_cambio_rollback = filter_telegram(filter_hora_rollback, 'Coordinador cambio*+')
        fecha_programada_rollback = filter_telegram(filter_hora_rollback, 'Fecha programada de inicio+')
        fecha_programada_fin_rollback = filter_telegram(filter_hora_rollback, 'Fecha programada de finalización+')
        rollback_rollback = filter_telegram(filter_hora_rollback, 'Inicio Rollback')
        resp_otecel_rollback = filter_telegram(filter_hora_rollback, 'Resp Otecel*')

        if len(id_cambio_rollback) > 0:
            ChatTelegram(
                f'🔴 Validacion Rollback de actividad:\n{id_cambio_rollback},\n'
                f'🔴 Estado:\n{estado_rollback},\n'
                f'🔴 Clase:\n{clase_rollback},\n'
                f'🔴 Resumen:\n{resumen_rollback},\n'
                f'🔴 horario de rollback:\n{rollback_rollback},\n'
                f'⚠️ Confirma si es necesario su ejecucion o no'
            )

        # print(frame_add_colum)
        return filter_hora_programada, filter_hora_programada_final, filter_hora_rollback


# path = ExtractData(path_temp())
# path.data_matriz('11:35')

if __name__ == '__main__':
    ExtractData()
