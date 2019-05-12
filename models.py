def salary_proj(avg):
    r = 0.004
    multiplier = 1.1
    start = 0.7*avg
    s_max = multiplier * float(avg)
    out = []
    for t in range(0, 31):
        denom = 1.00 + (s_max / (float(start) - 1))**(-r*s_max*t)
        out.append(s_max/denom)
    return out

def loan_division(annual_loan_burden, sub_eligible, college_term, dependent):
    loans = {}
    for year in range(college_term):
        loans[int(year)] = {'Subsidized':0, 'Unsubsidized':0, 'Private':0}

    if sub_eligible and dependent:
        sub_max = 23000
        unsub_max = 8000
        sub_yearly_max = [3500, 4500, 5500]
        unsub_yearly_max = [2000, 2000, 2000]
    elif not sub_eligible and dependent:
        sub_max = 0
        unsub_max = 31000
        sub_yearly_max = [0, 0, 0]
        unsub_yearly_max = [5500, 6500, 7500]
    elif sub_eligible and not dependent:
        sub_max = 23000
        unsub_max = 34500
        sub_yearly_max = [3500, 4500, 5500]
        unsub_yearly_max = [6000, 6000, 7000]
    else:
        sub_max = 0
        unsub_max = 57500
        sub_yearly_max = [0, 0, 0]
        unsub_yearly_max = [9500, 10500, 12500]

    for year in range(college_term):
        sample_burden = annual_loan_burden
        if year < 2:
            loan_index = year
        else:
            loan_index = 2

        if sample_burden <= sub_yearly_max[loan_index]:
            loans[year]['Subsidized'] = sample_burden
            sub_max -= sample_burden
        elif sample_burden > sub_yearly_max[loan_index] and sample_burden < (sub_yearly_max[loan_index] + unsub_yearly_max[loan_index]):
            loans[year]['Subsidized'] = sub_yearly_max[loan_index]
            loans[year]['Unsubsidized'] = sample_burden - sub_yearly_max[loan_index]
            sub_max -= sub_yearly_max[loan_index]
            unsub_max -= (sample_burden - sub_yearly_max[loan_index])
        elif sample_burden > (sub_yearly_max[loan_index] + unsub_yearly_max[loan_index]):
            loans[year]['Subsidized'] = sub_yearly_max[loan_index]
            loans[year]['Unsubsidized'] = unsub_yearly_max[loan_index]
            loans[year]['Private'] = sample_burden - sub_yearly_max[loan_index] - unsub_yearly_max[loan_index]
            sub_max -= sub_yearly_max[loan_index]
            unsub_max -= unsub_yearly_max[loan_index]

        if sub_max < sub_yearly_max[loan_index]:
            sub_yearly_max[loan_index] = sub_max
        if unsub_max < unsub_yearly_max[loan_index]:
            unsub_yearly_max[loan_index] = unsub_max

    return loans

loans = loan_division(40000, True, 4, True)
for key, value in loans.items():
    print value
loans = loan_division(40000, True, 6, True)
for key, value in loans.items():
    print value
