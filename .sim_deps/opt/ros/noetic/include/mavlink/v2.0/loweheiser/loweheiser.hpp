/** @file
 *	@brief MAVLink comm protocol generated from loweheiser.xml
 *	@see http://mavlink.org
 */

#pragma once

#include <array>
#include <cstdint>
#include <sstream>

#ifndef MAVLINK_STX
#define MAVLINK_STX 253
#endif

#include "../message.hpp"

namespace mavlink {
namespace loweheiser {

/**
 * Array of msg_entry needed for @p mavlink_parse_char() (through @p mavlink_get_msg_entry())
 */
constexpr std::array<mavlink_msg_entry_t, 3> MESSAGE_ENTRIES {{ {0, 50, 9, 9, 0, 0, 0}, {300, 217, 22, 22, 0, 0, 0}, {10151, 195, 85, 85, 0, 0, 0} }};

//! MAVLINK VERSION
constexpr auto MAVLINK_VERSION = 2;


// ENUM DEFINITIONS


/** @brief  */
enum class MAV_CMD
{
    LOWEHEISER_SET_STATE=10151, /* Set Loweheiser desired states |EFI Index| Desired Engine/EFI State (0: Power Off, 1:Running)| Desired Governor State (0:manual throttle, 1:Governed throttle)| Manual throttle level, 0% - 100%| Electronic Start up (0:Off, 1:On)| Empty| Empty|  */
};

//! MAV_CMD ENUM_END
constexpr auto MAV_CMD_ENUM_END = 10152;


} // namespace loweheiser
} // namespace mavlink

// MESSAGE DEFINITIONS
#include "./mavlink_msg_loweheiser_gov_efi.hpp"

// base include
#include "../minimal/minimal.hpp"
