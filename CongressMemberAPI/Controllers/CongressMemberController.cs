using Microsoft.AspNetCore.Mvc;
using Newtonsoft.Json;
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
        [ProducesResponseType(typeof(CongressMember), StatusCodes.Status200OK)]
        public async ValueTask<IActionResult> CreateOrUpdate(CongressMember congressMember)
        {
            _logger.LogInformation($"[POST Request] {JsonConvert.SerializeObject(congressMember)}");

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

            _logger.LogInformation($"Request successful, returning: {JsonConvert.SerializeObject(updatedCongressMember)}");
            return CreatedAtAction(nameof(Get), new { id = updatedCongressMember.ID }, updatedCongressMember);
        }

        [HttpGet("{id:int}")]
        [ProducesResponseType(typeof(CongressMember), StatusCodes.Status200OK)]
        public async ValueTask<IActionResult> Get(int id)
        {
            _logger.LogInformation($"[GET Request] id = {id}");

            CongressMember? congressMember = null;
            try
            {
                congressMember = await _congressMemberService.RetrieveCongressMemberAsync(id);
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

            _logger.LogInformation($"Request successful, returning: {JsonConvert.SerializeObject(congressMember)}");
            return Ok(congressMember);
        }

        [HttpGet]
        [ProducesResponseType(typeof(IQueryable<CongressMember>), StatusCodes.Status200OK)]
        public IActionResult GetAll()
        {
            _logger.LogInformation("[GET Request] id = all");

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

            _logger.LogInformation("Request successful");
            return Ok(congressMembers);
        }

        [HttpDelete("{id:int}")]
        [ProducesResponseType(typeof(CongressMember), StatusCodes.Status200OK)]
        public async ValueTask<IActionResult> Delete(int id)
        {
            _logger.LogInformation($"[DELETE Request] id = {id}");

            var congressMember = await _congressMemberService.DeleteCongressMemberAsync(id);
            if (congressMember is null)
            {
                return NotFound();
            }

            _logger.LogInformation($"Request successful, returning: {JsonConvert.SerializeObject(congressMember)}");
            return Ok(congressMember);
        }
    }
}