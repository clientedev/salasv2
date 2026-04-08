from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import io
from datetime import datetime
from datetime import datetime

def create_header_style():
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#2c3e50')
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=20,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#34495e')
    )
    
    return title_style, subtitle_style

def add_header(story, title, subtitle=None, school_name='SENAI'):
    title_style, subtitle_style = create_header_style()
    
    # School Header
    header_text = f"""
    <para align="center">
    <font size="20" color="#1e3a8a"><b>ESCOLA {school_name.upper()}</b></font><br/>
    <font size="12" color="#475569">Sistema de Gestão de Salas</font>
    </para>
    """
    story.append(Paragraph(header_text, getSampleStyleSheet()['Normal']))
    story.append(Spacer(1, 20))
    
    # Title
    story.append(Paragraph(title, title_style))
    
    if subtitle:
        story.append(Paragraph(subtitle, subtitle_style))
    
    story.append(Spacer(1, 20))

def generate_classroom_pdf(classroom, schedules, school_name='SENAI'):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    
    story = []
    styles = getSampleStyleSheet()
    
    # Header
    add_header(story, f"Relatório da Sala: {classroom.name}", school_name=school_name)
    
    # Classroom Information
    info_data = [
        ['Campo', 'Informação'],
        ['Nome da Sala', classroom.name],
        ['Capacidade', f'{classroom.capacity} alunos'],
        ['Bloco', classroom.block],
        ['Possui Computadores', 'Sim' if classroom.has_computers else 'Não'],
        ['Softwares Instalados', classroom.software or 'Nenhum'],
        ['Descrição', classroom.description or 'Sem descrição']
    ]
    
    info_table = Table(info_data, colWidths=[2*inch, 4*inch])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
    ]))
    
    story.append(info_table)
    story.append(Spacer(1, 30))
    
    # Occupancy Statistics
    total_slots = 23  # 6 days * 4 shifts - 1 (no Saturday night)
    occupied_slots = len(schedules)
    occupancy_rate = (occupied_slots / total_slots * 100) if total_slots > 0 else 0
    
    story.append(Paragraph("<b>Taxa de Ocupação</b>", styles['Heading3']))
    story.append(Spacer(1, 12))
    
    occupancy_data = [
        ['Métrica', 'Valor'],
        ['Total de Horários Possíveis', f'{total_slots} horários'],
        ['Horários Ocupados', f'{occupied_slots} horários'],
        ['Horários Livres', f'{total_slots - occupied_slots} horários'],
        ['Taxa de Ocupação', f'{occupancy_rate:.1f}%']
    ]
    
    occupancy_table = Table(occupancy_data, colWidths=[2.5*inch, 2*inch])
    occupancy_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#10b981')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f0fdf4')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bbf7d0')),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
    ]))
    
    story.append(occupancy_table)
    story.append(Spacer(1, 30))
    
    # Schedule Information
    if schedules:
        story.append(Paragraph("<b>Horários de Aula</b>", styles['Heading3']))
        story.append(Spacer(1, 12))
        
        days = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
        
        schedule_data = [['Dia', 'Turno', 'Horário', 'Curso', 'Instrutor']]
        
        shifts = {'morning': 'Manhã', 'afternoon': 'Tarde', 'fullday': 'Integral', 'night': 'Noite'}
        
        for schedule in schedules:
            # Truncate long course names to prevent text overlap
            course_name = schedule.course_name
            if len(course_name) > 20:
                course_name = course_name[:17] + "..."
            
            instructor = schedule.instructor or 'N/A'
            if len(instructor) > 12:
                instructor = instructor[:9] + "..."
            
            schedule_data.append([
                days[schedule.day_of_week],
                shifts.get(schedule.shift, schedule.shift.title()),
                f'{schedule.start_time} - {schedule.end_time}',
                course_name,
                instructor
            ])
        
        schedule_table = Table(schedule_data, colWidths=[0.9*inch, 0.9*inch, 1.1*inch, 1.8*inch, 1.1*inch])
        schedule_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('TOPPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8fafc')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ]))
        
        story.append(schedule_table)
    else:
        story.append(Paragraph("<b>Horários de Aula</b>", styles['Heading3']))
        story.append(Paragraph("Nenhum horário cadastrado para esta sala.", styles['Normal']))
    
    # Footer
    story.append(Spacer(1, 50))
    footer_text = f"Relatório gerado em {datetime.now().strftime('%d/%m/%Y às %H:%M')}"
    story.append(Paragraph(footer_text, styles['Normal']))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

def generate_general_report(classrooms, all_schedules, school_name='SENAI'):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    
    story = []
    styles = getSampleStyleSheet()
    
    # Header
    add_header(story, "Relatório Geral de Salas", f"Total de {len(classrooms)} salas cadastradas", school_name=school_name)
    
    # Create schedule map for quick lookup
    schedule_map = {}
    for schedule in all_schedules:
        if schedule.classroom_id not in schedule_map:
            schedule_map[schedule.classroom_id] = []
        schedule_map[schedule.classroom_id].append(schedule)
    
    # Detailed report for each classroom
    for i, classroom in enumerate(classrooms):
        if i > 0:
            story.append(Spacer(1, 30))
        
        # Classroom header
        classroom_title = f"Sala: {classroom.name}"
        story.append(Paragraph(classroom_title, styles['Heading2']))
        story.append(Spacer(1, 12))
        
        # Basic info
        info_data = [
            ['Informação', 'Detalhes'],
            ['Nome', classroom.name],
            ['Capacidade', f'{classroom.capacity} alunos'],
            ['Localização', classroom.block],
            ['Computadores', 'Sim' if classroom.has_computers else 'Não'],
        ]
        
        if classroom.software:
            info_data.append(['Software', classroom.software])
        
        info_table = Table(info_data, colWidths=[1.5*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#f8fafc'), colors.white]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e5e7eb')),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        
        story.append(info_table)
        story.append(Spacer(1, 15))
        
        # Occupancy statistics for this classroom
        classroom_schedules = schedule_map.get(classroom.id, [])
        total_slots = 23  # 6 days * 4 shifts - 1 (no Saturday night)
        occupied_slots = len(classroom_schedules)
        occupancy_rate = (occupied_slots / total_slots * 100) if total_slots > 0 else 0
        
        occupancy_data = [
            ['Métrica', 'Valor'],
            ['Horários Ocupados', f'{occupied_slots} de {total_slots}'],
            ['Taxa de Ocupação', f'{occupancy_rate:.1f}%'],
            ['Status', 'Em uso' if occupied_slots > 0 else 'Disponível']
        ]
        
        occupancy_table = Table(occupancy_data, colWidths=[1.5*inch, 2*inch])
        occupancy_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#10b981')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#f0fdf4'), colors.white]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#bbf7d0')),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        
        story.append(occupancy_table)
        story.append(Spacer(1, 15))
        
        # Schedule details for this classroom
        if classroom_schedules:
            story.append(Paragraph("Horários Detalhados", styles['Heading3']))
            story.append(Spacer(1, 8))
            
            days = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado']
            shifts = {'morning': 'Manhã', 'afternoon': 'Tarde', 'fullday': 'Integral', 'night': 'Noite'}
            
            schedule_data = [['Dia', 'Turno', 'Curso', 'Instrutor', 'Horário']]
            
            for schedule in sorted(classroom_schedules, key=lambda x: (x.day_of_week, x.shift)):
                course_name = schedule.course_name
                if len(course_name) > 20:
                    course_name = course_name[:17] + "..."
                
                instructor = schedule.instructor or 'N/A'
                if len(instructor) > 15:
                    instructor = instructor[:12] + "..."
                
                schedule_data.append([
                    days[schedule.day_of_week],
                    shifts.get(schedule.shift, schedule.shift),
                    course_name,
                    instructor,
                    f'{schedule.start_time} - {schedule.end_time}'
                ])
            
            schedule_table = Table(schedule_data, colWidths=[0.8*inch, 0.8*inch, 1.8*inch, 1.2*inch, 1*inch])
            schedule_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 8),
                ('FONTSIZE', (0, 1), (-1, -1), 7),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#f8fafc'), colors.white]),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
                ('LEFTPADDING', (0, 0), (-1, -1), 4),
                ('RIGHTPADDING', (0, 0), (-1, -1), 4),
                ('TOPPADDING', (0, 0), (-1, -1), 3),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ]))
            
            story.append(schedule_table)
        else:
            empty_style = ParagraphStyle(
                'Empty',
                parent=styles['Normal'],
                fontSize=9,
                textColor=colors.HexColor('#64748b'),
                spaceAfter=15
            )
            story.append(Paragraph("Nenhum horário cadastrado para esta sala.", empty_style))
    
    # Footer
    story.append(Spacer(1, 30))
    footer_text = f"Relatório gerado em {datetime.now().strftime('%d/%m/%Y às %H:%M')}"
    story.append(Paragraph(footer_text, styles['Normal']))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

def generate_availability_report(classrooms, schedules, school_name='SENAI'):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    
    story = []
    styles = getSampleStyleSheet()
    
    # Header
    add_header(story, "Relatório de Disponibilidade de Salas", school_name=school_name)
    
    days = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado']
    shifts = ['morning', 'afternoon', 'fullday', 'night']
    shift_names = {'morning': 'Manhã', 'afternoon': 'Tarde', 'fullday': 'Integral', 'night': 'Noite'}
    
    # Create schedule map
    schedule_map = {}
    for schedule in schedules:
        key = (schedule.classroom_id, schedule.day_of_week, schedule.shift)
        schedule_map[key] = schedule
    
    for day_idx, day_name in enumerate(days):
        story.append(Paragraph(f"<b>{day_name}</b>", styles['Heading3']))
        story.append(Spacer(1, 12))
        
        # Create availability table for this day
        data = [['Sala'] + [shift_names[shift] for shift in shifts]]
        
        for classroom in classrooms:
            row = [f"{classroom.name} ({classroom.block})"]
            
            for shift in shifts:
                # Skip night shift for Saturday
                if day_idx == 5 and shift == 'night':
                    row.append('N/A')
                    continue
                    
                key = (classroom.id, day_idx, shift)
                if key in schedule_map:
                    schedule = schedule_map[key]
                    row.append(f"OCUPADA\n{schedule.course_name}")
                else:
                    row.append("LIVRE")
            
            data.append(row)
        
        table = Table(data, colWidths=[2*inch, 1.2*inch, 1.2*inch, 1.2*inch, 1.2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#7c3aed')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        # Color coding for availability
        for row_idx in range(1, len(data)):
            for col_idx in range(1, len(data[row_idx])):
                cell_value = data[row_idx][col_idx]
                if 'LIVRE' in cell_value:
                    table.setStyle(TableStyle([
                        ('BACKGROUND', (col_idx, row_idx), (col_idx, row_idx), colors.HexColor('#dcfce7'))
                    ]))
                elif 'OCUPADA' in cell_value:
                    table.setStyle(TableStyle([
                        ('BACKGROUND', (col_idx, row_idx), (col_idx, row_idx), colors.HexColor('#fecaca'))
                    ]))
                elif 'N/A' in cell_value:
                    table.setStyle(TableStyle([
                        ('BACKGROUND', (col_idx, row_idx), (col_idx, row_idx), colors.HexColor('#f3f4f6'))
                    ]))
        
        story.append(table)
        story.append(Spacer(1, 20))
    
    # Legend
    story.append(Paragraph("<b>Legenda:</b>", styles['Heading4']))
    legend_data = [
        ['Status', 'Cor', 'Significado'],
        ['LIVRE', '', 'Sala disponível para uso'],
        ['OCUPADA', '', 'Sala com aula agendada'],
        ['N/A', '', 'Turno não disponível']
    ]
    
    legend_table = Table(legend_data, colWidths=[1*inch, 0.8*inch, 2.5*inch])
    legend_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#374151')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (1, 1), (1, 1), colors.HexColor('#dcfce7')),
        ('BACKGROUND', (1, 2), (1, 2), colors.HexColor('#fecaca')),
        ('BACKGROUND', (1, 3), (1, 3), colors.HexColor('#f3f4f6')),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
    ]))
    
    story.append(legend_table)
    
    # Footer
    story.append(Spacer(1, 30))
    footer_text = f"Relatório gerado em {datetime.now().strftime('%d/%m/%Y às %H:%M')}"
    story.append(Paragraph(footer_text, styles['Normal']))
    
    doc.build(story)
    buffer.seek(0)
    return buffer
