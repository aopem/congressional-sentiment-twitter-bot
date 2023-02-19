using Microsoft.AspNetCore.Mvc;
using CongressMemberTrackingService.Models;
using CongressMemberTrackingService.Services;

namespace CongressMemberTrackingService.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class CongressMemberTrackingController : ControllerBase
    {
        private readonly ILogger<CongressMemberTrackingController> _logger;
        private readonly CongressMemberService _congressMemberService;

        public CongressMemberTrackingController(
            ILogger<CongressMemberTrackingController> logger,
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