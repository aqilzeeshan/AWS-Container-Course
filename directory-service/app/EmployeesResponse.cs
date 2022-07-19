using System;
using System.Collections.Generic;

namespace DirectoryService
{
    public class EmployeesResponse
    {
        public EmployeesResponse() {
            Message = $"Hello from {Environment.MachineName}";
        }

        public string Message { get; set; }

        public IEnumerable<Employee> Employees { get; set; }
    }
}
