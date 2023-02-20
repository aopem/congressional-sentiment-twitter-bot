using Microsoft.AspNetCore.Mvc;
using CongressMemberService.Models;
using CongressMemberService.Services;

namespace CongressMemberAPI.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class CongressMemberController : ControllerBase
    {
        private readonly ILogger<CongressMemberController> _logger;
        private readonly CongressMemberService _congressMemberService;

        public CongressMemberController(
            ILogger<CongressMemberController> logger,
            CongressMemberService congressMemberService)
        {
            _logger = logger;
            _congressMemberService = congressMemberService;
        }

        [HttpPost]
        public async ValueTask<CongressMember> CreateOrUpdate(CongressMember congressMember)
        {
            return await _congressMemberService.CreateCongressMemberAsync(congressMember);
        }

        [HttpGet]
        public IQueryable<CongressMember> Get()
        {
            return _congressMemberService.RetrieveAllCongressMembersAsync();
        }

        [HttpGet]
        public async ValueTask<CongressMember> GetAll(Guid id)
        {
            return await _congressMemberService.RetrieveCongressMemberAsync(id);
        }

        [HttpDelete]
        public async ValueTask<CongressMember> Delete(Guid id)
        {
            return await _congressMemberService.DeleteCongressMemberAsync(id);
        }
    }
}