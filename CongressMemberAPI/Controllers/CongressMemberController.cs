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
            var message = $"[POST Request] {congressMember.ToString()}";
            _logger.LogInformation(message);

            var updatedCongressMember = new CongressMember();
            try
            {
                updatedCongressMember = await _congressMemberService.CreateCongressMemberAsync(congressMember);
            }
            catch (Exception e)
            {
                _logger.LogError(e.Message);
                return StatusCode(StatusCodes.Status500InternalServerError, e.Message);
            }

            return CreatedAtAction(nameof(Get), new { id = updatedCongressMember.ID }, updatedCongressMember);
        }

        [HttpGet("{id:int}")]
        public async ValueTask<IActionResult> Get(int id)
        {
            var message = $"[GET Request] id = {id}";
            _logger.LogInformation(message);

            CongressMember? congressMember = null;
            try
            {
                await _congressMemberService.RetrieveCongressMemberAsync(id);
            }
            catch (Exception e)
            {
                _logger.LogError(e.Message);
                return StatusCode(StatusCodes.Status500InternalServerError, e.Message);
            }

            if (congressMember is null)
            {
                return NotFound();
            }

            return Ok(congressMember);
        }

        [HttpGet]
        public IActionResult GetAll()
        {
            var message = "[GET Request] id = all";
            _logger.LogInformation(message);

            IQueryable<CongressMember>? congressMembers = null;
            try
            {
                congressMembers = _congressMemberService.RetrieveAllCongressMembers();
            }
            catch (Exception e)
            {
                _logger.LogError(e.Message);
                return StatusCode(StatusCodes.Status500InternalServerError, e.Message);
            }

            if (congressMembers is null)
            {
                return NotFound();
            }

            return Ok(congressMembers);
        }

        [HttpDelete("{id:int}")]
        public async ValueTask<IActionResult> Delete(int id)
        {
            var message = $"[DELETE Request]id = {id}";
            _logger.LogInformation(message);

            var congressMember = await _congressMemberService.DeleteCongressMemberAsync(id);
            if (congressMember is null)
            {
                return NotFound();
            }

            return Ok(congressMember);
        }
    }
}