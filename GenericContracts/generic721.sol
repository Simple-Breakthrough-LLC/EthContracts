import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

contract GenericERC721 is ERC721 {
	constructor() ERC721("name", "symbol") {}

	function mint(
        address to,
        uint256 id
        )
		public {
		_safeMint(to, id);
	}
}
