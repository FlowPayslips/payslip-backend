# payslip-backend

### The Process() algorithm
For a given payrun:
For each onboarded, active employee in the company:
1. Fetch active EmployeeSalaryComponents
2. If none exist → error (rollback everything)
3. Create Payslip with zeroed totals
4. For each component:
- Create PayslipLineItem (snapshot)
- Accumulate earnings or deductions
5. Update Payslip totals
6. After all employees succeed → mark payrun PROCESSED
All inside one transaction.