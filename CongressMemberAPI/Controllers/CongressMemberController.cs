using Microsoft.AspNetCore.Mvc;
using Common.Models;
using CongressMemberAPI.Services;

namespace CongressMemberAPI.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
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
        public async ValueTask<IActionResult> CreateOrUpdate(CongressMember congressMember)
        {
            var updatedCongressMember = await _congressMemberService.CreateCongressMemberAsync(congressMember);
            return CreatedAtAction(nameof(Get), new { id = updatedCongressMember.ID }, updatedCongressMember);
        }

        [HttpGet("{id:int}")]
        public async ValueTask<IActionResult> Get(int id)
        {
            var congressMember = await _congressMemberService.RetrieveCongressMemberAsync(id);
            if (congressMember is null)
            {
                return NotFound();
            }

            return Ok(congressMember);
        }

        [HttpGet]
        public IActionResult GetAll()
        {
            return Ok(_congressMemberService.RetrieveAllCongressMembers());
        }

        [HttpDelete("{id:int}")]
        public async ValueTask<IActionResult> Delete(int id)
        {
            var congressMember = await _congressMemberService.DeleteCongressMemberAsync(id);
            if (congressMember is null)
            {
                return NotFound();
            }

            return Ok(congressMember);
        }
    }
}