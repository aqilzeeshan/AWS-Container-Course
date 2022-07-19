using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Amazon;
using Amazon.DynamoDBv2;
using Amazon.DynamoDBv2.Model;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;

namespace DirectoryService.Controllers
{
    [ApiController]
    public class EmployeeController : ControllerBase
    {
        private AmazonDynamoDBClient _dynamoDBClient;
        private readonly ILogger<EmployeeController> _logger;

        public EmployeeController(ILogger<EmployeeController> logger)
        {
            _logger = logger;
            AmazonDynamoDBConfig dynamoDBConfig = new AmazonDynamoDBConfig();
            dynamoDBConfig.MaxErrorRetry = 2;
            if(!String.IsNullOrEmpty(Environment.GetEnvironmentVariable("DYNAMO_ENDPOINT_OVERRIDE"))) {
                dynamoDBConfig.ServiceURL = Environment.GetEnvironmentVariable("DYNAMO_ENDPOINT_OVERRIDE");
            }
            _dynamoDBClient = new AmazonDynamoDBClient(dynamoDBConfig);
        }

        [HttpGet]
        [Route("[controller]")]
        public async Task<EmployeesResponse> Get()
        {
            var scan  = await _dynamoDBClient.ScanAsync(new ScanRequest{
                TableName = "Employees"
            });
            return new EmployeesResponse {
                Employees = scan.Items.Select(item => new Employee
                {
                    Id = item["id"].S,
                    Fullname = item["full_name"].S,
                    JobTitle = item["job_title"].S,
                    Location = item["location"].S,
                    Badges = item["badges"].SS,
                })
                .OrderBy(emp => emp.Fullname)
                .ToArray()
            };
        }

        [HttpGet]
        [Route("[controller]/{id}")]
        public async Task<EmployeeResponse> GetOne(string id)
        {
            var query = await _dynamoDBClient.GetItemAsync(new GetItemRequest{
                Key = new Dictionary<string, AttributeValue>() { {"id", new AttributeValue { S=id } } },
                TableName = "Employees"
            });
            return new EmployeeResponse {
                Employee = new Employee
                {
                    Id = query.Item["id"].S,
                    Fullname = query.Item["full_name"].S,
                    JobTitle = query.Item["job_title"].S,
                    Location = query.Item["location"].S,
                    Badges = query.Item["badges"].SS
                }
            };
        }

        [HttpPost]
        [Route("[controller]")]
        public async Task<EmployeeResponse> Create(Employee employee)
        {
            employee.Id = System.Guid.NewGuid().ToString();
            await _dynamoDBClient.PutItemAsync(new PutItemRequest{
                TableName="Employees",
                Item=new Dictionary<string, AttributeValue>() {
                    {"id", new AttributeValue { S = employee.Id} },
                    {"full_name", new AttributeValue { S = employee.Fullname } },
                    {"job_title", new AttributeValue { S = employee.JobTitle } },
                    {"location", new AttributeValue { S = employee.Location } },
                    {"badges", new AttributeValue { SS = employee.Badges } }
                }
            });
            return new EmployeeResponse { Employee = employee };
        }

        [HttpPut]
        [Route("[controller]")]
        public async Task<EmployeeResponse> Update(Employee employee)
        {
            await _dynamoDBClient.UpdateItemAsync(new UpdateItemRequest{
                TableName="Employees",
                Key=new Dictionary<string, AttributeValue>() {
                    {"id", new AttributeValue { S = employee.Id } },
                },
                ExpressionAttributeNames = new Dictionary<string, string> {
                    {"#loc", "location"}
                },
                ExpressionAttributeValues = new Dictionary<string, AttributeValue> {
                    { ":fn" , new AttributeValue { S = employee.Fullname } },
                    { ":jt", new AttributeValue { S = employee.JobTitle } },
                    { ":loc", new AttributeValue { S = employee.Location } },
                    { ":bg", new AttributeValue { SS = employee.Badges } }
                },
                UpdateExpression = "SET full_name = :fn, job_title = :jt, #loc = :loc, badges = :bg"
            });
            return new EmployeeResponse { Employee = employee };
        }


        [HttpDelete]
        [Route("[controller]/id")]
        public async Task<bool> Delete(string id)
        {
            await _dynamoDBClient.DeleteItemAsync(new DeleteItemRequest {
                TableName="Employees",
                Key=new Dictionary<string, AttributeValue>() {
                    {"id", new AttributeValue { S = id } },
                }
            });
            return true;
        }
    }
}
