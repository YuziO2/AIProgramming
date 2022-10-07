class Convert:
  # 转换工作：
  def Job(job):
    jobs = ['admin.', 'blue-collar', 'entrepreneur', 'housemaid', 'management', 'retired', 'self-employed',
            'services', 'student', 'technician', 'unemployed', 'unknown']
    for i in range(len(jobs)):
      if jobs[i] == job:
        return i

  # 转换婚姻：
  def Marital(marital):
    maritals = ['single', 'married', 'divorced', 'unknown']
    for i in range(len(maritals)):
      if maritals[i] == marital:
        return i

  # 转换学历：
  def Education(education):
    educations = ['illiterate', 'basic.4y', 'basic.6y', 'basic.9y',
                  'high.school', 'university.degree', 'professional.course', 'unknown']
    for i in range(len(educations)):
      if educations[i] == education:
        return i

  # 转换二元数据
  def Binary(arg):
    binary = ['no', 'yes', 'unknown']
    contact = ['cellular', 'telephone']
    poutcome = ['failure', 'success', 'nonexistent']
    for i in range(len(binary)):
      if binary[i] == arg:
        return i
    for i in range(len(contact)):
      if contact[i] == arg:
        return i
    for i in range(len(poutcome)):
      if poutcome[i] == arg:
        return i

  # 转换月份
  def Month(month):
    months = ['jan', 'feb', 'mar', 'apr', 'may',
              'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    for i in range(len(months)):
      if months[i] == month:
        return i

  # 转换星期
  def Day(day):
    days = ['mon', 'tue', 'wed', 'thu', 'fri']
    for i in range(len(days)):
      if days[i] == day:
        return i
