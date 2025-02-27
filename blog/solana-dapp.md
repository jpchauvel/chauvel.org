---
blogpost: true
date: 27 Feb, 2025
author: hellhound
location: Lima, Perú
category: Blockchain
tags: blockchain, solana, dapp, anchor, anchorpy, rust, python
language: English
---

# Creating a Simple Solana dApp with Anchor and AnchorPy

![Solana](/_static/images/solana.png){ align=center width=400px }

Me and a couple of friends decided to embark on a project related to the Solana
blockchain. Long story short, I managed to create a simple dApp using Anchor and
AnchorPy.

## Why Solana?

Solana is a blockchain platform that is built on top of the Solana runtime. It
is a high-performance blockchain that is designed to be used for building
decentralized applications.

Transactions on Solana take on average 400ms, which is a lot faster than other
blockchains like Ethereum. That's one of the key factors why we, as a team,
selected Solana as a platform to build our dApp on.

## The Proof-of-Concept dApp

I created a simple dApp consisted of an Anchor-based (written in Rust) Solana
Program and an AnchorPy client that was used to interact with the Solana
Program.  The smart contract (Solana Program) was design to only write a message
into a Solana account using a concept known as PDA (Program Derived Address).

### What is a Program Derived Address?

Program Derived Addresses (PDAs) provide developers on Solana with two main use
cases:

* **Deterministic Account Addresses**: PDAs provide a mechanism to
  deterministically derive an address using a combination of optional "seeds"
(predefined inputs) and a specific program ID. 

* **Enable Program Signing**: The Solana runtime enables programs to "sign" for
  PDAs which are derived from its program ID.  You can think of PDAs as a way to
create hashmap-like structures on-chain from a predefined set of inputs (e.g.
strings, numbers, and other account addresses).

The benefit of this approach is that it eliminates the need to keep track of an
exact address. Instead, you simply need to recall the specific inputs used for
its derivation.

![PDA](/_static/images/pda.png){ align=center width=700px }

It's important to understand that simply deriving a Program Derived Address
(PDA) does not automatically create an on-chain account at that address.
Accounts with a PDA as the on-chain address must be explicitly created through
the program used to derive the address. You can think of deriving a PDA as
finding an address on a map. Just having an address does not mean there is
anything built at that location.

PDAs are addresses that are deterministically derived and look like standard
public keys, but have no associated private keys. This means that no external
user can generate a valid signature for the address. However, the Solana runtime
enables programs to programmatically "sign" for PDAs without needing a private
key.

For context, Solana Keypairs are points on the Ed25519 curve (elliptic-curve
cryptography) which have a public key and corresponding private key. We often
use public keys as the unique IDs for new on-chain accounts and private keys for
signing.

## The Solana Program

The Solana Program is written in Rust and is a simple program that writes a
message into a Solana account using a Program Derived Address (PDA). The message
is a string that is passed as an argument to the program using the AnchorPy
client (which I will cover next). The program resizes the PDA acocunt based on
the length of the message and clears the previous content of the data (message)
before writing the new one.

This program is devided into three public functions:

* `pub fn create_account(ctx: Context<CreatePDA>, nonce: u64, message: String) -> Result<()>`:
This function initializes the PDA account and writes the message into it.

```rust
pub fn create_account(ctx: Context<CreatePDA>, nonce: u64, message: String) -> Result<()> {
    let pda = &mut ctx.accounts.pda_account;
    pda.authority = ctx.accounts.user.key();
    pda.nonce = nonce;
    pda.data = message.into_bytes(); // Store the message in data

    msg!(
        "Created PDA with message: {}",
        String::from_utf8_lossy(&pda.data)
    );
    Ok(())
}
```

* `pub fn resize_account(ctx: Context<ResizePDA>, new_size: u64) -> Result<()>`:
This function resizes the PDA account based on the new size.

```rust
pub fn resize_account(ctx: Context<ResizePDA>, new_size: u64) -> Result<()> {
    let account_info = &mut ctx.accounts.pda_account.to_account_info();
    let old_size = account_info.try_data_len()? as u64;
    let new_data_size = 8 + 32 + 8 + 4 + new_size as u64;

    let rent = Rent::get()?;
    let new_minimum_balance = rent.minimum_balance(new_data_size as usize);

    if new_data_size > old_size {
        let required_lamports = new_minimum_balance.saturating_sub(account_info.lamports());

        // Log current balances for inspection
        msg!(
            "Current Authority Lamports: {}",
            ctx.accounts.authority.lamports()
        );
        msg!("Current PDA Account Lamports: {}", account_info.lamports());
        msg!("Required for resize: {}", required_lamports);

        if required_lamports > 0 {
            require!(
                ctx.accounts.authority.lamports() >= required_lamports,
                ErrorCode::InsufficientFunds
            );

            let cpi_accounts = Transfer {
                from: ctx.accounts.authority.to_account_info(),
                to: account_info.clone(),
            };
            let cpi_context =
                CpiContext::new(ctx.accounts.system_program.to_account_info(), cpi_accounts);
            system_program::transfer(cpi_context, required_lamports)?;

            msg!(
                "After transfer Authority Lamports: {}",
                ctx.accounts.authority.lamports()
            );
            msg!(
                "After transfer PDA Account Lamports: {}",
                account_info.lamports()
            );
        }
    } else if new_data_size < old_size {
        // Resize smaller, refunding lamports
        let refund = account_info.lamports().saturating_sub(new_minimum_balance);
        **ctx.accounts.authority.try_borrow_mut_lamports()? += refund;
        **account_info.try_borrow_mut_lamports()? -= refund;
        msg!("Decreasing size, refunding lamports: {}", refund);
    }

    account_info.realloc(new_data_size as usize, false)?;

    let pda_data = &mut &mut ctx.accounts.pda_account.data;
    pda_data.resize(new_size as usize, 0);

    msg!("Resized PDA from {} to {} bytes", old_size, new_size);
    Ok(())
}
```

* `pub fn update_data(ctx: Context<UpdatePDA>, new_message: String) -> Result<()>)`:
This function updates the data of the PDA account with the new message.

```rust
pub fn update_data(ctx: Context<UpdatePDA>, new_message: String) -> Result<()> {
    let pda = &mut ctx.accounts.pda_account;
    let new_data = new_message.into_bytes();

    require!(new_data.len() <= pda.data.len(), ErrorCode::DataTooLarge);

    pda.data.clear(); // Clear the existing data
    pda.data.extend(new_data); // Add new data

    msg!(
        "Updated PDA with new message: {}",
        String::from_utf8_lossy(&pda.data)
    );
    Ok(())
}
```

## The PDA Account

The PDA account contains the authority address, nonce, and data. The authority
address is the public key of the user who created the PDA. The nonce is a
counter that is incremented each time the PDA is resized. The data is the
message that is stored in the PDA account.

```rust
#[account]
pub struct PDAAccount {
    pub authority: Pubkey,
    pub nonce: u64,
    pub data: Vec<u8>, // Stores the message as bytes
}
```

## The CreatePDA Context

The `CreatePDA` context is used to create a new PDA account and write a message
into it. This context is the main one, basically, because it contains the seed
of the PDA account.

```rust
#[derive(Accounts)]
#[instruction(nonce: u64, message: String)]
pub struct CreatePDA<'info> {
    #[account(
        init,
        payer = user,
        space = 8 + 32 + 8 + 4 + message.len(), // Base size + message size
        seeds = [b"my-seed", user.key().as_ref(), &nonce.to_le_bytes()],
        bump
    )]
    pub pda_account: Account<'info, PDAAccount>,

    #[account(mut)]
    pub user: Signer<'info>,

    pub system_program: Program<'info, System>,
}
```

The seed is a combination of a constant byte string and the concatenation of the
user's public key and the nonce. The nonce is a counter that is incremented each
time the PDA is resized. The message is the string that is passed as an argument
to the program and is stored in the PDA account, which is used to reserve space
for it.

## The AnchorPy Client

This script is designed to streamline the process of creating, managing, and
retrieving data from PDAs, leveraging the capabilities of the AnchorPy
framework.

**Environment Setup and Configuration**: The script sets up the necessary
environment by loading key components of the Solana infrastructure. It connects
to the Solana Devnet and utilizes a locally stored keypair for signing
transactions, ensuring secure and authenticated blockchain interactions.

```python
PROJECT_PATH: str = os.path.realpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
)
SEED_PREFIX: bytes = b"my-seed"
DEVNET_URL: str = "https://api.devnet.solana.com"


async def async_main(message: str, nonce: int) -> None:
    """Main function to handle Solana interactions."""
    # Load the Anchor program
    workspace: WorkspaceType = create_workspace(PROJECT_PATH, url=DEVNET_URL)
    program: Program = workspace["resizable_pda"]

    # Check if PDA exists; create or update accordingly
    await check_and_create_or_update_pda(program, nonce, message)

    # Close the client connection
    await close_workspace(workspace)
```

**PDA Derivation and Management**: Central to the script's functionality is its
ability to derive and manage PDAs. Using functions like `derive_pda()`, it
calculates the PDA based on a seed, user public key, and nonce, ensuring unique
and consistent address generation. The script transitions from addressing
routines to executing actions:

```python
async def derive_pda(program: Program, nonce: int) -> Pubkey:
    """Derives the PDA address using the seed, user pubkey, and nonce."""
    pda, _ = Pubkey.find_program_address(
        [
            SEED_PREFIX,
            bytes(program.provider.wallet.public_key),
            nonce.to_bytes(8, "little"),
        ],
        program.program_id,
    )
    return pda
```


- **Account Creation**: The `create_pda()` function instantiates new PDA
  accounts, initializing them with a stored message. This feature is pivotal for
applications that depend on storing and retrieving user or application data on
the blockchain.

```python
async def create_pda(program: Program, nonce: int, message: str) -> None:
    """Creates a PDA account and stores the initial message."""
    pda: Pubkey = await derive_pda(program, nonce)

    tx: Signature = await program.rpc["create_account"](
        nonce,
        message,
        ctx=Context(
            accounts={
                "pda_account": pda,
                "user": program.provider.wallet.public_key,
                "system_program": SYSTEM_PROGRAM_ID,  # System Program ID
            },
            signers=[user],
        ),
    )

    print(f"PDA Created: {pda} | Transaction: {tx}")

    # Retrieve and print the stored message
    _ = await get_pda_message(program, pda)
```

- **Dynamic Updating**: With the `update_pda()` function, the script simplifies
  updating existing PDA data. It checks the current data size and resizes the
PDA storage dynamically if necessary, ensuring efficient use of resources and
effortless data management.

```python
async def update_pda(program: Program, nonce: int, new_message: str) -> None:
    """Resizes the PDA (if necessary) and updates the stored message."""
    pda: Pubkey = await derive_pda(program, nonce)

    # Fetch the current PDA account data
    try:
        account: Container[bytes] = await program.account["PDAAccount"].fetch(
            pda
        )
        current_size: int = len(account.data)
    except AccountDoesNotExistError:
        print(f"Error: PDA {pda} does not exist. Cannot update.")
        return

    new_size: int = len(new_message)

    # Resize the PDA only if the new message is larger than the current storage
    if new_size > current_size:
        print(f"Resizing PDA from {current_size} to {new_size} bytes...")
        tx_resize: Signature = await program.rpc["resize_account"](
            new_size,
            ctx=Context(
                accounts={
                    "pda_account": pda,
                    "authority": program.provider.wallet.public_key,
                    "system_program": SYSTEM_PROGRAM_ID,  # System Program ID
                },
                signers=[user],
            ),
        )
        print(f"PDA Resized | Transaction: {tx_resize}")

        # Wait for confirmation before updating
        await asyncio.sleep(1)

    # Now, update the stored message
    tx_update: Signature = await program.rpc["update_data"](
        new_message,
        ctx=Context(
            accounts={
                "pda_account": pda,
                "authority": program.provider.wallet.public_key,
            },
            signers=[user],
        ),
    )

    print(
        f"PDA Updated with message: {new_message} | Transaction: {tx_update}"
    )

    # Retrieve and print the updated message
    _ = await get_pda_message(program, pda)
```

**Data Retrieval**: The `get_pda_message()` function provides an easy method to
fetch and display messages stored within PDAs. By decoding the stored data and
removing padding, the function ensures that the retrieved information is
user-friendly and immediately useful.

```python
async def get_pda_message(program: Program, pda: Pubkey) -> str | None:
    """Fetches the stored message from the PDA."""
    try:
        account: Container[bytes] = await program.account["PDAAccount"].fetch(
            pda
        )
        stored_message: str = (
            bytes(account.data).decode("utf-8").rstrip("\x00")
        )  # Decode and remove padding
        print(f"Retrieved PDA Message: {stored_message}")
        return stored_message
    except AccountDoesNotExistError:
        print(f"No PDA found at {pda}, needs creation.")
        return None
```

**Automated Workflow**: The script assess the existence of a PDA and determine
the appropriate action autonomously. The `check_and_create_or_update_pda()`
function orchestrates this flow, deciding whether to create a new account or
update an existing one.

```python
async def check_and_create_or_update_pda(
    program: Program, nonce: int, message: str
) -> None:
    """Checks if PDA exists. If not, creates it; otherwise, updates it."""
    pda: Pubkey = await derive_pda(program, nonce)

    stored_message: str | None = await get_pda_message(program, pda)

    if stored_message is None:
        # PDA does not exist, create it
        await create_pda(program, nonce, message)
    else:
        # PDA exists, update it
        await update_pda(program, nonce, message)
```

**Intuitive CLI**: The AnchorPy Client is wrapped in a command-line interface
using Typer. This design allows to execute operations directly from their
terminal, simply by providing messages and nonce values as input arguments. It
reduces the need for intricate code management and makes the script accessible
to a broader audience.

```python
@app.command()
def main(
    message: str = typer.Argument(
        ..., help="The message to store in the PDA."
    ),
    nonce: int = typer.Option(
        1, help="The nonce for PDA derivation (default: 1)."
    ),
) -> None:
    """CLI command to create or update a PDA with a given message."""
    asyncio.run(async_main(message, nonce))
```

## Conclusion

Building a decentralized application (dApp) on the Solana blockchain using
Anchor and AnchorPy offers a streamlined and efficient development process.
Leveraging the high-speed transactions characteristic of the Solana network,
developers can create responsive applications that enhance user experience.
Utilizing Program-Derived Addresses (PDAs), the application can
deterministically organize and manage on-chain data without the need for complex
address management. The Rust-based Solana Program facilitates secure and
optimized operations, while the Python-based AnchorPy client provides a
flexible, user-friendly interface for interacting with smart contracts. This
approach offers a robust framework for developing scalable blockchain solutions
capable of meeting diverse application needs. Whether for financial
applications, identity management, or generalized data storage, this setup opens
new avenues for innovation in blockchain technology.

```{note}
You can find the complete code here: https://github.com/jpchauvel/resizable_pda
```
